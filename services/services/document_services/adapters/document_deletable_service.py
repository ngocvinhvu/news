from typing import Type, Union, List

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pymongo.client_session import ClientSession

from common import (
    AsyncGenerated,
    GeneratedExecutor,
    SettableGenerated,
    GeneratedException)
from services.common import (
    AsyncModelDeletable,
    AsyncModelExecutable)
from services.exceptions import NotFoundException
from services.services.document_services.generated import (
    DocumentDeletable,
    DocumentGettable)


class DocumentDeletableService(AsyncModelDeletable, AsyncModelExecutable):
    def __init__(self, document_type: Type[Document],
                 session: ClientSession = None,
                 additions: dict = None):
        self.__session = session
        self.__additions = additions
        self.__document_type = document_type

    async def execute(self, *args, **kwargs):
        return await self.delete(*args, **kwargs)

    async def delete(self, model_id: str, **kwargs):
        pre_generated_services: List[Union[SettableGenerated, AsyncGenerated]] = (
            kwargs.get('pre_generated_services', []))

        document_gettable = DocumentGettable(self.__document_type, PydanticObjectId(model_id),
                                             addition=self.__additions,
                                             session=self.__session)
        document_deletable = DocumentDeletable(session=self.__session)
        try:
            return await GeneratedExecutor([document_gettable, *pre_generated_services, document_deletable]).generate()
        except GeneratedException:
            raise NotFoundException(model_id)
