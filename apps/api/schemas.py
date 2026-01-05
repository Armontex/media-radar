from pydantic import BaseModel, ConfigDict
from .enums import Source


class TitleSchema(BaseModel):
    external_id: int
    name: str
    descr: str = ""
    cover_url: str = ""
    source: Source
    is_active: bool = True


class Image(BaseModel):
    medium: str

    model_config = ConfigDict(extra="ignore")


class Show(BaseModel):
    id: int
    name: str
    image: Image
    summary: str
    status: str
    model_config = ConfigDict(extra="ignore")


class TVMazeTitleSchema(BaseModel):
    show: Show
    model_config = ConfigDict(extra="ignore")
