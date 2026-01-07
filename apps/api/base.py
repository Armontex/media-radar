from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from .schemas import TitleSchema


class ContentProvider(ABC):

    @abstractmethod
    def get_titles(self, query: str) -> Iterable[TitleSchema]:
        pass

    @abstractmethod
    def get_parts(self, title_id: int):
        pass
