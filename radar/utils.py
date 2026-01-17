import requests
import json
import hashlib
import hmac
from django.http import HttpRequest
from typing import NamedTuple, Literal, Callable, Iterable, TypeVar
from apps.providers.tvmaze import TitleSchema
from apps.core.config import settings
from apps.core.logger import logger


T = TypeVar("T")
TitleKey = tuple[str, int]


class TitleContext(NamedTuple):
    action: Literal["add", "delete", "not_auth"]
    title: TitleSchema


def built_titles_context(titles: Iterable[T],
                         *,
                         mapper: Callable[[T], TitleSchema],
                         subscribed: Iterable[TitleKey],
                         is_authenticated: bool) -> Iterable[TitleContext]:
    result = []

    for t in titles:
        title = mapper(t)

        if not is_authenticated:
            action = "not_auth"
        else:
            key = (title.source.value, title.external_id)
            action = "delete" if key in subscribed else "add"
        result.append(TitleContext(action, title))

    return result


def check_captcha(token: str, ip: str):
    resp = requests.post("https://smartcaptcha.cloud.yandex.ru/validate",
                         data={
                             "secret":
                             settings.CAPTCHA_SERVER_KEY.get_secret_value(),
                             "token":
                             token,
                             "ip":
                             ip
                         },
                         timeout=1)
    server_output = resp.content.decode()
    if resp.status_code != 200:
        logger.warning(
            f"Allow access due to an error: code={resp.status_code}; message={server_output}",
        )
        return True
    return json.loads(server_output)["status"] == "ok"


def get_client_ip(request: HttpRequest) -> str | None:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def verify_telegram_auth(data: dict, bot_token: str) -> bool:
    hash_received = data.pop('hash')
    check_list = [f"{k}={v}" for k, v in sorted(data.items())]
    data_check_string = "\n".join(check_list).encode()
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated = hmac.new(secret_key, data_check_string,
                          hashlib.sha256).hexdigest()
    return calculated == hash_received
