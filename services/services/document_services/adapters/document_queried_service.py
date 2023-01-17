from abc import ABC, abstractmethod
from typing import Type, List, Tuple

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from beanie.odm.fields import SortDirection
from pymongo.client_session import ClientSession

from services.common import AsyncModelGettable, AsyncModelListable
from services.exceptions import NotFoundException
from services.services.document_services.generated import (
    DocumentGettable,
    DocumentFindable,
    DocumentCountable)


class AsyncModelQueryable(AsyncModelGettable, AsyncModelListable, ABC):
    @abstractmethod
    async def list(self, attributes: dict,
                   limit: int = 20,
                   offset: int = 0,
                   sorts: Tuple[str, SortDirection] = None,
                   **kwargs) -> List[Document]:
        pass

    @abstractmethod
    async def count(self, attributes: dict) -> int:
        pass


class DocumentQueriedService(AsyncModelQueryable):
    def __init__(self, document_type: Type[Document],
                 projection_model: Type[Document] = None,
                 session: ClientSession = None,
                 addition: dict = None):
        self.__session = session
        self.__addition = addition
        self.__document_type = document_type
        self.__projection_model = projection_model

    async def count(self, attributes: dict) -> int:
        return await DocumentCountable(self.__document_type, attributes,
                                       addition=self.__addition,
                                       session=self.__session).generate()

    async def list(self, attributes: dict,
                   limit: int = 20,
                   offset: int = 0,
                   sorts: List[Tuple[str, SortDirection]] = None, **kwargs) -> List[Document]:
        return await DocumentFindable(self.__document_type, attributes,
                                      limit=limit,
                                      sorts=sorts,
                                      offset=offset,
                                      session=self.__session,
                                      addition=self.__addition,
                                      projection_model=self.__projection_model).generate()

    async def get(self, model_id: str, **kwargs) -> Document:
        document = await DocumentGettable(self.__document_type, PydanticObjectId(model_id),
                                          projection_model=self.__projection_model,
                                          addition=self.__addition,
                                          session=self.__session).generate()
        if not document:
            raise NotFoundException(model_id)
        return document
