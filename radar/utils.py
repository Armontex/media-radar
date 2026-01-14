from typing import NamedTuple, Literal
from apps.providers.tvmaze import TitleSchema
from .models import Profile
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
