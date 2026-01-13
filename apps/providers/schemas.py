from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .enums import Source


class TitleSchema(BaseModel):
    external_id: int
    name: str
    descr: str | None
    cover_url: str | None
    source: Source
    is_active: bool = True


class ReleaseSchema(BaseModel):
    external_title_id: int
    external_release_id: int
    name: str | None
    number: int | None
    season: int | None
    released_at: datetime | None
    descr: str | None


class Image(BaseModel):
    medium: str | None = None

    model_config = ConfigDict(extra="ignore")


class ShowTitle(BaseModel):
    id: int
    name: str
    image: Image | None = None
    summary: str | None = None
    status: str | None = None
    model_config = ConfigDict(extra="ignore")


class TVMazeTitleSchema(BaseModel):
    show: ShowTitle
    model_config = ConfigDict(extra="ignore")


class TVMazeEpisodeSchema(BaseModel):
    id: int
    name: str | None = None
    season: int | None = None
    number: int | None = None
    summary: str | None = None
    airstamp: datetime | None = None

    model_config = ConfigDict(extra="ignore")


class TVMazeShowSchema(BaseModel):
    id: int
    name: str
    status: str | None = None
    image: Image | None = None
    summary: str | None = None

    model_config = ConfigDict(extra="ignore")
