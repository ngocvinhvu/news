from typing import Any
from uuid import uuid4

from pymongo.client_session import ClientSession

from common import (
    AsyncSettableGenerated,
    ResultSettableService)
from services.services.document_services import DocumentUpdatable


class AccountDeletable(AsyncSettableGenerated):
    def __init__(self,
                 session: ClientSession = None,
                 account=None):
        self.__session = session
        self.__generated = ResultSettableService(account)

    def set_result(self, account):
        self.__generated.set_result(account)

    async def generate(self) -> Any:
        # Soft delete
        attributes = {
            'phone': str(uuid4()),
            'email': str(uuid4()),
            'deleted': True
        }

        return await DocumentUpdatable(attributes, session=self.__session,
                                       document=self.__generated.generate()).generate()
