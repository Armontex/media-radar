from ..utils.http import HTTPClient, UrlRedactor


class TelegramMailer:

    BASE_URL = "https://api.telegram.org/"
    SEND_TEXT_PATH = "/bot{token}/sendMessage"
    SEND_PHOTO_PATH = "/bot{token}/sendPhoto"

    def __init__(self, token: str) -> None:
        self._token = token

    def _send_text(self, chat_id: int, text: str) -> None:
        with HTTPClient(self.BASE_URL, redactor=UrlRedactor()) as client:
            client.post(self.SEND_TEXT_PATH.format(token=self._token),
                        json={
                            "chat_id": chat_id,
                            "text": text
                        })

    def _send_photo(self,
                    chat_id: int,
                    *,
                    image_url: str,
                    caption: str = "") -> None:
        with HTTPClient(self.BASE_URL, redactor=UrlRedactor()) as client:
            client.post(self.SEND_PHOTO_PATH.format(token=self._token),
                        json={
                            "chat_id": chat_id,
                            "photo": image_url,
                            "caption": caption,
                        })

    def send(self,
             chat_id: int,
             *,
             text: str,
             image_url: str | None = None) -> None:
        if not image_url:
            self._send_text(chat_id, text=text)
            return
        self._send_photo(chat_id, image_url=image_url, caption=text)
