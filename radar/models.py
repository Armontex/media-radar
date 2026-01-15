from django.db import models
from django.conf import settings
from .choices import SourceChoices, NotifyChannelChoices, StatusChoices


class Title(models.Model):
    name = models.CharField("Название", max_length=255)
    descr = models.TextField("Описание", null=True, blank=True)
    cover_url = models.URLField("Ссылка на обложку", null=True, blank=True)

    external_id = models.IntegerField("EXTERNAL_ID")
    source = models.CharField("Источник",
                              choices=SourceChoices.choices,
                              max_length=25)

    is_active = models.BooleanField("Статус мониторинга", default=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "external_id"],
                                    name="uniq_title_source_external"),
        ]


class Release(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="releases",
        verbose_name="Тайтл",
    )

    name = models.CharField("Название", max_length=255, null=True, blank=True)
    number = models.IntegerField("Номер", null=True, blank=True)
    season = models.IntegerField("Сезон", null=True, blank=True)

    released_at = models.DateTimeField("Дата выхода", null=True, blank=True)
    descr = models.TextField("Описание", null=True, blank=True)

    external_release_id = models.IntegerField("EXTERNAL_ID")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "external_release_id"],
                                    name="uniq_release_title_external")
        ]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    email = models.EmailField("EMAIL")
    telegram_id = models.IntegerField("TELEGRAM_ID",
                                      unique=True,
                                      null=True,
                                      default=None)
    register_at = models.DateTimeField("Дата регистрации", auto_now_add=True)
    main_channel = models.CharField("Основной канал уведомлений",
                                    choices=NotifyChannelChoices.choices,
                                    default=NotifyChannelChoices.EMAIL)


class Subscription(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Профиль",
        blank=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="subscriptions",
                              verbose_name="Тайтл")

    is_active = models.BooleanField("Статус мониторинга",
                                    default=True,
                                    null=False)
    created_at = models.DateTimeField("Дата подписки", auto_now_add=True)

    last_notified_release = models.ForeignKey(
        Release,
        on_delete=models.SET_NULL,
        related_name="subscriptions",
        verbose_name="Последнее уведомление о релизе",
        null=True,
        blank=True,
        default=None,
    )
    notify_channel = models.CharField("Канал уведомлений",
                                      choices=NotifyChannelChoices.choices,
                                      default=NotifyChannelChoices.EMAIL,
                                      max_length=24)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "title"],
                                    name="uniq_subscription_profile_title"),
        ]


class NotificationLog(models.Model):

    profile = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                related_name="notification_logs",
                                verbose_name="Профиль",
                                null=True,
                                blank=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name="notification_logs",
                              verbose_name="Тайтл")

    release = models.ForeignKey(Release,
                                on_delete=models.DO_NOTHING,
                                related_name="notification_logs",
                                verbose_name="Релиз")

    notify_channel = models.CharField("Канал уведомлений",
                                      choices=NotifyChannelChoices.choices,
                                      max_length=24)
    status = models.CharField("Статус уведомления",
                              choices=StatusChoices.choices,
                              default=StatusChoices.AWAIT)
    sent_at = models.DateTimeField("Дата отправления", null=True, default=None)
