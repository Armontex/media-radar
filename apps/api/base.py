from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from .schemas import TitleSchema, ReleaseSchema


class ContentProvider(ABC):

    @abstractmethod
    def get_titles(self, query: str) -> Iterable[TitleSchema]:
        pass
    
    @abstractmethod
    def get_title(self, title_id: int) -> TitleSchema:
        pass

    @abstractmethod
    def get_parts(self, title_id: int) -> list[ReleaseSchema]:
        pass