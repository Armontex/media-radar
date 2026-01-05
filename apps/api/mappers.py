from .schemas import TVMazeTitleSchema, TitleSchema
from .enums import Source

def map_tvmazeschema_to_title(tvmaze_schema: TVMazeTitleSchema) -> TitleSchema:
    return TitleSchema(
        external_id=tvmaze_schema.show.id,
        name=tvmaze_schema.show.name,
        descr=tvmaze_schema.show.summary,
        cover_url=tvmaze_schema.show.image.medium,
        source=Source.TVMAZE,
        is_active=tvmaze_schema.show.status != "Ended"
    )