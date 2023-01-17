from typing import Type, Union, List

from beanie import Document
from pymongo.client_session import ClientSession

from common import (
    AsyncGenerated,
    GeneratedExecutor,
    SettableGenerated)
from services.common import (
    AsyncModelCreatable,
    AsyncModelExecutable)
from services.services.document_services.generated import DocumentCreatable


class DocumentCreatableService(AsyncModelCreatable, AsyncModelExecutable):
    def __init__(self, document_type: Type[Document],
                 session: ClientSession = None):
        self.__session = session
        self.__document_type = document_type

    async def execute(self, *args, **kwargs):
        return await self.create(*args, **kwargs)

    async def create(self, attributes: dict, **kwargs):
        pre_generated_services: List[Union[SettableGenerated, AsyncGenerated]] = (
            kwargs.get('pre_generated_services', []))

        document_creatable = DocumentCreatable(self.__document_type, attributes=attributes, session=self.__session)
        return await GeneratedExecutor([*pre_generated_services, document_creatable]).generate()
