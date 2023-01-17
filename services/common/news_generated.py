from abc import abstractmethod, ABC
from typing import List

from common import AsyncGenerated
from pydantic import BaseModel


class NewsIn(BaseModel):
    html: str
    image_url: str
    detail_url: str
    summary: str
    description: str
    publisher_id: str
    category_id: str


class NewsExecutable(ABC):
    @abstractmethod
    def execute(self, raw: dict) -> List[AsyncGenerated]:
        pass
