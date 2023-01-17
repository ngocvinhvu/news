from copy import deepcopy
from hashlib import md5
from typing import Any

from pymongo.client_session import ClientSession

from common import (
    AsyncSettableGenerated,
    ResultSettableService)
from services.services.document_services import DocumentUpdatable


class AccountUpdatable(AsyncSettableGenerated):
    def __init__(self, attributes: dict,
                 session: ClientSession = None,
                 account=None):
        self.__session = session
        self.__attributes = attributes

        self.__generated = ResultSettableService(account)

    def set_result(self, account):
        self.__generated.set_result(account)

    async def generate(self) -> Any:
        attributes = deepcopy(self.__attributes)

        password = attributes.get('password')
        if password:
            attributes['password'] = md5(password.encode()).hexdigest()

        return await DocumentUpdatable(attributes, session=self.__session,
                                       document=self.__generated.generate()).generate()
