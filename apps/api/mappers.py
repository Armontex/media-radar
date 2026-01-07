from .schemas import TVMazeTitleSchema, TitleSchema, TVMazeEpisodeSchema, ReleaseSchema
from .enums import Source


def map_tvmaze_schema_to_title(
        tvmaze_schema: TVMazeTitleSchema) -> TitleSchema:
    return TitleSchema(
        external_id=tvmaze_schema.show.id,
        name=tvmaze_schema.show.name,
        descr=tvmaze_schema.show.summary,
        cover_url=tvmaze_schema.show.image.medium,  # type: ignore
        source=Source.TVMAZE,
        is_active=tvmaze_schema.show.status != "Ended")


def map_tvmaze_ep_schema_to_release(tvmaze_ep_shema: TVMazeEpisodeSchema,
                                    title_id: int) -> ReleaseSchema:
    return ReleaseSchema(external_title_id=title_id,
                         name=tvmaze_ep_shema.name,
                         number=tvmaze_ep_shema.number,
                         season=tvmaze_ep_shema.season,
                         released_at=tvmaze_ep_shema.airstamp,
                         descr=tvmaze_ep_shema.summary,
                         external_release_id=tvmaze_ep_shema.id)
