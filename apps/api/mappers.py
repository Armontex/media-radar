from .schemas import TVMazeTitleSchema, TitleSchema, TVMazeEpisodeSchema, ReleaseSchema, TVMazeShowSchema
from .enums import Source


def map_tvmaze_schema_to_title(
        tvmaze_schema: TVMazeTitleSchema) -> TitleSchema:
    return TitleSchema(external_id=tvmaze_schema.show.id,
                       name=tvmaze_schema.show.name,
                       descr=tvmaze_schema.show.summary,
                       cover_url=tvmaze_schema.show.image.medium
                       if tvmaze_schema.show.image else None,
                       source=Source.TVMAZE,
                       is_active=tvmaze_schema.show.status != "Ended")


def map_tvmaze_show_schema_to_title(
        tvmaze_schema: TVMazeShowSchema) -> TitleSchema:
    return TitleSchema(
        external_id=tvmaze_schema.id,
        name=tvmaze_schema.name,
        descr=tvmaze_schema.summary,
        cover_url=tvmaze_schema.image.medium if tvmaze_schema.image else None,
        source=Source.TVMAZE,
        is_active=tvmaze_schema.status != "Ended")


def map_tvmaze_ep_schema_to_release(tvmaze_ep_shema: TVMazeEpisodeSchema,
                                    title_id: int) -> ReleaseSchema:
    return ReleaseSchema(external_title_id=title_id,
                         name=tvmaze_ep_shema.name,
                         number=tvmaze_ep_shema.number,
                         season=tvmaze_ep_shema.season,
                         released_at=tvmaze_ep_shema.airstamp,
                         descr=tvmaze_ep_shema.summary,
                         external_release_id=tvmaze_ep_shema.id)
