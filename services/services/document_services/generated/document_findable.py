from typing import List, Tuple, Type

from beanie import Document
from beanie.odm.fields import SortDirection
from pymongo.client_session import ClientSession

from common import (
    ExecutableGeneratedService,
    AsyncSettableGenerated,
    ResultSettableService,
    ExecutableGenerated,
    AsyncGenerated)


class DocumentFindable(AsyncGenerated):
    def __init__(self, document_type: Type[Document], attributes: dict,
                 sorts: Tuple[str, SortDirection] = None,
                 projection_model: Type[Document] = None,
                 session: ClientSession = None,
                 addition: dict = None,
                 offset: int = -1,
                 limit: int = -1):

        self.__sorts = sorts
        self.__limit = limit
        self.__offset = offset
        self.__session = session
        self.__addition = addition
        self.__attributes = attributes
        self.__document_type = document_type
        self.__projection_model = projection_model or self.__document_type

    async def generate(self) -> List[Document]:
        query_attributes = dict(session=self.__session,
                                projection_model=self.__projection_model)

        if self.__sorts:
            query_attributes['sort'] = self.__sorts

        if self.__limit != -1:
            query_attributes['limit'] = self.__limit

        if self.__offset != -1:
            query_attributes['skip'] = self.__offset

        additions = self.__addition or {}
        return await (self.__document_type.find({**self.__attributes, **additions}, **query_attributes).to_list())


class DocumentIndexGettable(AsyncSettableGenerated, ExecutableGenerated):
    def __init__(self, document_type: Type[Document], attributes: dict,
                 projection_model: Type[Document] = None,
                 executed_services: List = None,
                 session: ClientSession = None):
        self.__session = session
        self.__attributes = attributes
        self.__document_type = document_type
        self.__projection_model = projection_model or document_type

        self.__settable = ResultSettableService()
        self.__generated = ExecutableGeneratedService(self.__settable, self,
                                                      executable_services=executed_services)

    async def execute_generated(self) -> Document:
        return await (self.__document_type.find(self.__attributes,
                                                session=self.__session,
                                                projection_model=self.__projection_model).first_or_none())

    def set_result(self, document: Document):
        self.__settable.set_result(document)

    async def generate(self) -> Document:
        return await self.__generated.generate()


class DocumentCountable(AsyncGenerated):
    def __init__(self, document_type: Type[Document], attributes: dict,
                 session: ClientSession = None,
                 addition: dict = None):
        self.__session = session
        self.__addition = addition
        self.__attributes = attributes
        self.__document_type = document_type

    async def generate(self) -> int:
        additions = self.__addition or {}
        return await (self.__document_type.find({**self.__attributes, **additions}, session=self.__session).count())
