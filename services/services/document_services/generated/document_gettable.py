from typing import Type

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pymongo.client_session import ClientSession

from common import (
    ExecutableGenerated,
    ResultSettableService,
    AsyncSettableGenerated,
    ExecutableGeneratedService)


class DocumentGettable(AsyncSettableGenerated, ExecutableGenerated):
    def __init__(self, document_type: Type[Document], document_id: PydanticObjectId | str,
                 projection_model: Type[Document] = None,
                 session: ClientSession = None,
                 document: Document = None,
                 addition: dict = None):
        self.__session = session
        self.__addition = addition
        self.__document_id = document_id
        self.__document_type = document_type
        self.__projection_model = projection_model or self.__document_type

        self.__settable = ResultSettableService(document)
        self.__generated = ExecutableGeneratedService(self.__settable, self)

    def set_result(self, document: Document):
        self.__settable.set_result(document)

    async def execute_generated(self) -> Document | None:
        document_id = self.__document_id
        if isinstance(document_id, str):
            document_id = PydanticObjectId(document_id)

        addition = self.__addition or {}
        return await (self.__document_type
                      .find({'_id': document_id, **addition},
                            session=self.__session,
                            projection_model=self.__projection_model)
                      .first_or_none())

    async def generate(self) -> Document:
        return await self.__generated.generate()
