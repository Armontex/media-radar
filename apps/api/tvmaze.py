from .schemas import TitleSchema, TVMazeTitleSchema
from .mappers import map_tvmazeschema_to_title
from .base import ContentProvider
from ..utils.http import HTTPClient

class TVMazeProvider(ContentProvider):
    
    API_BASE_URL = "https://api.tvmaze.com/"
    SHOWS_PATH = "search/shows"
    
    def __init__(self) -> None:
        pass
    
    def get_titles(self, query: str) -> list[TitleSchema]:
        # TODO: Проверка на пустой query
        
        with HTTPClient(self.API_BASE_URL) as client:
            response = client.get(self.SHOWS_PATH, params={
                "q": query.lower()
            })
            schemas = [TVMazeTitleSchema.model_validate(d) for d in response.json()]
            return [map_tvmazeschema_to_title(s) for s in schemas]
    
    def get_parts(self, title_id: int):
        raise NotImplementedError