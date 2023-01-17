from typing import List

from pymongo.client_session import ClientSession

from common import (
    ExecutableGenerated,
    ResultSettableService,
    AsyncSettableGenerated,
    ExecutableGeneratedService)
from models.auth import Account


class AccountIndexGettable(AsyncSettableGenerated, ExecutableGenerated):
    def __init__(self, attributes: dict, session: ClientSession = None,
                 executed_services: List = None):
        self.__session = session
        self.__attributes = attributes

        self.__settable = ResultSettableService()
        self.__generated = ExecutableGeneratedService(self.__settable, self,
                                                      executable_services=executed_services)

    async def execute_generated(self) -> Account:
        return await (Account.find(self.__attributes, session=self.__session).first_or_none())

    def set_result(self, account: Account):
        self.__settable.set_result(account)

    async def generate(self) -> Account:
        return await self.__generated.generate()
