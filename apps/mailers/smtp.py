import smtplib
from email.message import EmailMessage
from ..core.config import settings
from ..core.logger import logger


class SMTPMailer:

    def __init__(self, *, email_sender: str, app_password: str, host: str,
                 port: int) -> None:
        self._sender = email_sender
        self._app_password = app_password
        self._host = host
        self._port = port
        self._server = None

    def __enter__(self):
        self._server = smtplib.SMTP_SSL(self._host, self._port)
        self._server.login(self._sender, self._app_password)
        return self

    def __exit__(self, *args):
        if self._server:
            self._server.quit()
            self._server = None

    def send(self, message: EmailMessage):
        message["From"] = self._sender

        logger.info("Отправление письма",
                    extra={
                        "from": message["From"],
                        "to": message["To"],
                        "subject": message["Subject"],
                        "content": message[""]
                    })
        if not self._server:
            raise RuntimeError(
                "Нет подключения к серверу. Используйте контекстный менеджер 'with'"
            )
        self._server.send_message(message)


class GmailMailer(SMTPMailer):

    def __init__(self, email_sender: str, app_password: str) -> None:
        super().__init__(email_sender=email_sender,
                         app_password=app_password,
                         host=settings.EMAIL_HOST,
                         port=settings.EMAIL_PORT)
