import requests
import json
import hashlib
import hmac
from django.http import HttpRequest
from typing import NamedTuple, Literal
from apps.providers.tvmaze import TitleSchema
from apps.core.config import settings
from apps.core.logger import logger
from .models import Profile, Title
from .mappers import title_to_schema


class TitleContext(NamedTuple):
    action: Literal["add", "delete", "not_auth"]
    title: TitleSchema


def get_titles_context(titles: list[TitleSchema] | list[Title],
                       profile: Profile | None = None) -> list[TitleContext]:
    result: list[TitleContext] = []
    if profile:

        sub_titles: list[Title] = list(
            map(lambda x: x.title,
                profile.subscriptions.all()))  # type: ignore
        source_title_id = {}
        for t in sub_titles:
            if t.source in source_title_id:
                source_title_id[t.source].append(t.external_id)
            else:
                source_title_id.setdefault(t.source, [t.external_id])

        for t in titles:
            source = t.source if isinstance(t, Title) else t.source.value
            if source in source_title_id:
                if t.external_id in source_title_id[source]:
                    result.append(TitleContext("delete", t if isinstance(
                        t, TitleSchema) else title_to_schema(t)))
                    continue
            result.append(TitleContext("add", t if isinstance(
                t, TitleSchema) else title_to_schema(t)))
    else:
        for t in titles:
            result.append(TitleContext("not_auth", t if isinstance(
                t, TitleSchema) else title_to_schema(t)))
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


def get_client_ip(request: HttpRequest):
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
