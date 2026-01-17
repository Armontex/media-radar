from bs4 import BeautifulSoup
from email.message import EmailMessage
from ..core.constants import TEMPLATES_DIR


def _get_template(name: str) -> str:
    with open(TEMPLATES_DIR / (name + ".html"), "r", encoding="utf-8") as file:
        return file.read()


def fill_notify_template(title_name: str,
                         cover_url: str | None = None,
                         season: int | None = None,
                         number: int | None = None) -> str:
    template = BeautifulSoup(_get_template("notify"), "html.parser")

    name = template.find(class_="card-name")
    if not name:
        raise ValueError("Отсутсвует card-name.")

    name.string = title_name

    if cover_url:

        cover = template.find(class_="card-cover")
        if not cover:
            raise ValueError("Отсутсвует card-cover.")

        cover.attrs["src"] = cover_url

    if season and number:

        episode_info = template.find(class_="message-episode-info")
        if not episode_info:
            raise ValueError("Отсутсвует message-episode-info.")

        episode_info.string = f"Сезон: {season} | Серия: {number}"

    return str(template)


def build_email_message(to: str,
                        *,
                        title: str,
                        text_content: str = "",
                        html_content: str | None = None) -> EmailMessage:
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = title
    msg.set_content(text_content)
    if html_content:
        msg.add_alternative(html_content, subtype="html")
    return msg
