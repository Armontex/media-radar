from django.db import transaction
from django.utils import timezone
from typing import Callable

from radar.models import Title, Subscription, NotificationLog, Release, Profile
from radar.choices import StatusChoices, NotifyChannelChoices
from apps.providers import TVMazeProvider, ContentProvider
from apps.providers.enums import Source
from apps.mailers import GmailMailer, TelegramMailer
from apps.mailers.utils import build_email_message, fill_notify_template
from apps.core.config import settings
from apps.core.logger import logger


providers: dict[str, ContentProvider] = {
    Source.TVMAZE.value: TVMazeProvider()
}


class Notifier:

    def __init__(self, profile: Profile, title: Title, log: NotificationLog) -> None:
        self._profile = profile
        self._title = title
        self._log = log

        self._notifiers: dict[NotifyChannelChoices, Callable[[], bool]] = {
            NotifyChannelChoices.EMAIL: self.__notify_email,
            NotifyChannelChoices.TELEGRAM: self.__notify_telegram
        }

    def notify(self) -> bool:
        channel = NotifyChannelChoices(self._profile.main_channel)
        notifier = self._notifiers.get(channel)

        if not notifier:
            logger.error("Неизвестный канал уведомлений", extra={
                "channel": channel
            })
            return False

        return notifier()

    def __notify_email(self) -> bool:
        try:
            template = fill_notify_template(title_name=self._title.name,
                                            cover_url=self._title.cover_url,
                                            season=self._log.release.season,
                                            number=self._log.release.number)

            if not self._profile.email:
                raise ValueError(
                    f"У профиля с каналом '{self._profile.main_channel}' email: {self._profile.email}.")

            msg = build_email_message(
                self._profile.email,
                title="Уведомление о новом выпуске",
                text_content=f"Вышел новый выпуск по {self._title.name}!",
                html_content=template)

            with GmailMailer(email_sender=settings.EMAIL_SENDER,
                             app_password=settings.EMAIL_APP_PASSWORD.
                             get_secret_value()) as mailer:
                mailer.send(msg)

            self._log.status = StatusChoices.SUCCESSFUL
            return True
        except Exception:
            self._log.status = StatusChoices.ERROR
            return False

    def __notify_telegram(self) -> bool:
        mailer = TelegramMailer(settings.BOT_TOKEN.get_secret_value())

        try:
            text = f"""‼️ Уведомление о новом выпуске ‼️

[{self._title.name}]
Сезон: {self._log.release.season} | Серия: {self._log.release.number}
        """

            if self._profile.telegram_id:
                mailer.send(self._profile.telegram_id,
                            text=text,
                            image_url=self._title.cover_url)
                self._log.status = StatusChoices.SUCCESSFUL
                return True

            self._log.status = StatusChoices.ERROR
            return False
        except Exception:
            self._log.status = StatusChoices.ERROR
            return False


def sync_title_releases(title: Title) -> list[Release]:
    new_releases: list[Release] = []

    provider = providers.get(title.source)
    if not provider:
        logger.error(f"Неизвестный провайдер.", extra={
            "source": title.source,
        })
        raise NotImplementedError(f"Неизвестный source: {title.source}")

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

    return new_releases


def notify(sub: Subscription, release: Release):

    log = NotificationLog.objects.create(
        profile=sub.profile,
        title=sub.title,
        release=release,
        notify_channel=sub.profile.main_channel,
        sent_at=timezone.now(),
    )

    notifier = Notifier(sub.profile, sub.title, log)
    success = notifier.notify()

    if not success:
        log.status = StatusChoices.ERROR
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
