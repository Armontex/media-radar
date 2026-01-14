from django.db import transaction
from django.utils import timezone

from radar.models import Title, Subscription, NotificationLog, Release, Profile
from radar.choices import StatusChoices, NotifyChannelChoices
from apps.providers import TVMazeProvider, ContentProvider
from apps.mailers.smtp import GmailMailer
from apps.mailers.utils import build_email_message, fill_notify_template
from apps.core.config import settings

providers: list[ContentProvider] = [TVMazeProvider()]


def sync_title_releases(title: Title) -> list[Release]:
    new_releases: list[Release] = []

    for provider in providers:
        if provider.source == title.source:
            parts = provider.get_parts(title.external_id)

            for part in parts:
                release, created = Release.objects.get_or_create(
                    title=title,
                    external_release_id=part.external_release_id,
                    defaults={
                        "name": part.name,
                        "number": part.number,
                        "season": part.season,
                        "released_at": part.released_at,
                        "descr": part.descr,
                    },
                )
                if created:
                    new_releases.append(release)
            break
    else:
        raise NotImplementedError(f"Неизвестный source: {title.source}")

    return new_releases


def notify_email(profile: Profile, title: Title, log: NotificationLog) -> bool:
    try:
        template = fill_notify_template(title_name=title.name,
                                        cover_url=title.cover_url,
                                        season=log.release.season,
                                        number=log.release.number)
        msg = build_email_message(
            profile.email,
            title="Уведомление о новом выпуске",
            text_content=f"Вышел новый выпуск по {title.name}!",
            html_content=template)

        with GmailMailer(email_sender=settings.EMAIL_SENDER,
                         app_password=settings.EMAIL_APP_PASSWORD.
                         get_secret_value()) as mailer:
            mailer.send(msg)
        log.status = StatusChoices.SUCCESSFUL
        return True
    except Exception:
        log.status = StatusChoices.ERROR
        return False


def notify(sub: Subscription, release: Release) -> None:

    log = NotificationLog.objects.create(
        profile=sub.profile,
        title=sub.title,
        release=release,
        notify_channel=sub.notify_channel,
        sent_at=timezone.now(),
    )

    success = False
    if sub.notify_channel == NotifyChannelChoices.EMAIL:
        success = notify_email(sub.profile, sub.title, log)

    if not success:
        log.save(update_fields=["status"])
        return

    with transaction.atomic():
        sub.last_notified_release = release
        sub.save(update_fields=["last_notified_release"])
        log.save(update_fields=["status"])


def send_notifications():
    titles = (Title.objects.filter(is_active=True,
                                   subscriptions__is_active=True).distinct())

    for title in titles:
        new_releases = sync_title_releases(title)

        subs = Subscription.objects.filter(
            title=title,
            is_active=True,
            profile__isnull=False,
        )

        for sub in subs:

            releases_for_sub = [
                release for release in new_releases
                if release.released_at is not None
                and release.released_at >= sub.created_at
            ]

            releases_for_sub.sort(key=lambda r: r.released_at)  # type: ignore

            for release in releases_for_sub:
                last = sub.last_notified_release

                if last and last.released_at and last.released_at >= release.released_at:  # type: ignore
                    continue

                notify(sub, release)
