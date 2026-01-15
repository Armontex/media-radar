import requests
import json
from django.http import HttpRequest
from typing import NamedTuple, Literal
from apps.providers.tvmaze import TitleSchema
from apps.core.config import settings
from apps.core.logger import logger
from .models import Profile, Title


class TitleContext(NamedTuple):
    action: Literal["add", "delete", "not_auth"]
    title: TitleSchema | Title


def get_titles_context(titles: list[TitleSchema] | list[Title],
                       profile: Profile | None = None) -> list[TitleContext]:
    result = []
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
                    result.append(TitleContext("delete", t))
                    continue
            result.append(TitleContext("add", t))
    else:
        for t in titles:
            result.append(TitleContext("not_auth", t))
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
