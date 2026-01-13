from .schemas import TitleSchema, TVMazeTitleSchema, TVMazeEpisodeSchema, TVMazeShowSchema
from .mappers import map_tvmaze_schema_to_title, map_tvmaze_ep_schema_to_release, map_tvmaze_show_schema_to_title
from .base import ContentProvider
from ..utils.http import HTTPClient


class TVMazeProvider(ContentProvider):

    API_BASE_URL = "https://api.tvmaze.com/"
    SHOWS_PATH = "search/shows"
    SHOW_PATH = "shows/{title_id}"
    EPISODES_PATH = SHOW_PATH + "/episodes"

    def get_titles(self, query: str) -> list[TitleSchema]:
        with HTTPClient(self.API_BASE_URL) as client:
            response = client.get(self.SHOWS_PATH, params={"q": query.lower()})
            schemas = [
                TVMazeTitleSchema.model_validate(d) for d in response.json()
            ]
            return [map_tvmaze_schema_to_title(s) for s in schemas]

    def get_title(self, title_id: int) -> TitleSchema:
        with HTTPClient(self.API_BASE_URL) as client:
            response = client.get(self.SHOW_PATH.format(title_id=title_id))
            schema = TVMazeShowSchema.model_validate(response.json())
            return map_tvmaze_show_schema_to_title(schema)

    def get_parts(self, title_id: int):
        with HTTPClient(self.API_BASE_URL) as client:
            response = client.get(self.EPISODES_PATH.format(title_id=title_id))
            schemas = [
                TVMazeEpisodeSchema.model_validate(d) for d in response.json()
            ]
            return [
                map_tvmaze_ep_schema_to_release(s, title_id) for s in schemas
            ]
