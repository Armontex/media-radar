from .models import Title
from apps.providers.schemas import TitleSchema
from apps.providers.enums import Source


def title_to_schema_mapper(title: Title) -> TitleSchema:
    return TitleSchema(
        external_id=title.external_id,
        name=title.name,
        descr=title.descr,
        cover_url=title.cover_url,
        source=Source(title.source),
        is_active=title.is_active
    )
