from copy import deepcopy
from hashlib import md5
from uuid import uuid4

from pymongo.client_session import ClientSession

from common import (
    ExecutableGenerated,
    AsyncSettableGenerated,
    ResultSettableService,
    ExecutableGeneratedService)
from models.auth import Account
from services.services.document_services import DocumentCreatable


class AccountCreatable(AsyncSettableGenerated, ExecutableGenerated):
    def __init__(self, attributes: dict,
                 session: ClientSession = None,
                 account: Account = None):
        self.__session = session
        self.__attributes = attributes
        self.__settable = ResultSettableService(account)
        self.__generated = ExecutableGeneratedService(self.__settable, self)

    def set_result(self, account: Account):
        self.__settable.set_result(account)

    async def execute_generated(self) -> Account:
        attributes = deepcopy(self.__attributes)
        attributes['tenant_id'] = str(uuid4())

        password = str(self.__attributes['password'])
        attributes['password'] = md5(password.encode()).hexdigest()

        account_creatable = DocumentCreatable(Account, session=self.__session, attributes=attributes)
        return await account_creatable.execute_generated()

    async def generate(self) -> Account:
        return await self.__generated.generate()
