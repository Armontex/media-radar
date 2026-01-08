from django.db.models import TextChoices


class SourceChoices(TextChoices):
    TVMAZE = "TVMaze", "TVMAZE"


class NotifyChannelChoices(TextChoices):
    TELEGRAM = "telegram", "TELEGRAM"
    EMAIL = "email", "EMAIL"


class StatusChoices(TextChoices):
    NOT_SENT = "not_sent"
    SUCCESSFUL = "successful"
    ERROR = "error"
    AWAIT = "await"
