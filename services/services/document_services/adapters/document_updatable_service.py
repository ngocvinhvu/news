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
    AsyncModelUpdatable,
    AsyncModelExecutable)
from services.exceptions import NotFoundException
from services.services.document_services.generated import (
    DocumentUpdatable,
    DocumentGettable)


class DocumentUpdatableService(AsyncModelUpdatable, AsyncModelExecutable):
    def __init__(self, document_type: Type[Document],
                 session: ClientSession = None,
                 additions: dict = None):
        self.__session = session
        self.__additions = additions
        self.__document_type = document_type

    async def update(self, model_id: str, attributes: dict, **kwargs):
        pre_generated_services: List[Union[SettableGenerated, AsyncGenerated]] = (
            kwargs.get('pre_generated_services', []))

        document_gettable = DocumentGettable(self.__document_type, PydanticObjectId(model_id),
                                             addition=self.__additions,
                                             session=self.__session)
        document_updatable = DocumentUpdatable(attributes, session=self.__session)
        try:
            return await GeneratedExecutor([*pre_generated_services, document_gettable, document_updatable]).generate()
        except GeneratedException:
            raise NotFoundException(model_id)

    async def execute(self, *args, **kwargs):
        return await self.update(*args, **kwargs)
