from typing import Type

from beanie import Document
from pymongo.client_session import ClientSession

from common import (
    ExecutableGenerated,
    ResultSettableService,
    AsyncSettableGenerated,
    ExecutableGeneratedService)


class DocumentCreatable(AsyncSettableGenerated, ExecutableGenerated):
    def __init__(self, document_type: Type[Document],
                 session: ClientSession = None,
                 document: Document = None,
                 attributes: dict = None):
        self.__session = session
        self.__attributes = attributes or {}
        self.__document_type = document_type

        self.__settable = ResultSettableService(document)
        self.__generated = ExecutableGeneratedService(self.__settable, self)

    def set_result(self, document: Document):
        self.__settable.set_result(document)

    async def execute_generated(self) -> Document:
        document = self.__document_type(**self.__attributes)
        await document.insert(session=self.__session)

        return document

    async def generate(self) -> Document:
        return await self.__generated.generate()

    def set_attributes(self, attributes: dict):
        self.__attributes = attributes

    def set_document_type(self, document_type: Type[Document]):
        self.__document_type = document_type
