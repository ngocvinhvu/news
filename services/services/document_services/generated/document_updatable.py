from beanie import Document
from pymongo.client_session import ClientSession

from common import (
    ResultSettableService,
    AsyncSettableGenerated)


class DocumentUpdatable(AsyncSettableGenerated):
    def __init__(self, attributes: dict,
                 session: ClientSession = None,
                 document: Document = None):
        self.__session = session
        self.__attributes = attributes
        self.__generated = ResultSettableService(document)

    def set_result(self, document: Document):
        self.__generated.set_result(document)

    async def generate(self) -> Document:
        document: Document = self.__generated.generate()
        await document.set(self.__attributes, session=self.__session)
        return document
