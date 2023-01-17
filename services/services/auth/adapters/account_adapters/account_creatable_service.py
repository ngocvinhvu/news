from pymongo.client_session import ClientSession

from common import (
    GeneratedExecutor,
    HandledGenerated,
    ResultGenerated)
from models.auth import Account
from services.common import AsyncModelCreatable
from services.exceptions import UniqueException
from services.services.auth.generated import (
    AccountIndexGettable,
    AccountCreatable)


class DuplicatedEmailHandler(ResultGenerated):
    def __init__(self, key: str, value: str):
        self.__key = key
        self.__value = value

    def generated_result(self, account: Account | None) -> Account | None:
        if account:
            raise UniqueException(f'Existed {self.__key}: {self.__value}')

        return account


class AccountCreatableService(AsyncModelCreatable):
    def __init__(self, session: ClientSession = None):
        self.__session = session

    async def create(self, attributes: dict, **kwargs) -> Account:
        email = attributes['email']
        phone = attributes['phone']

        email_gettable = AccountIndexGettable({'email': email},
                                              session=self.__session,
                                              executed_services=[HandledGenerated(
                                                  DuplicatedEmailHandler('email', email))])
        phone_gettable = AccountIndexGettable({'phone': phone},
                                              session=self.__session,
                                              executed_services=[HandledGenerated(
                                                  DuplicatedEmailHandler('phone number', phone))])

        account_creatable = AccountCreatable(attributes, session=self.__session)

        return await GeneratedExecutor([email_gettable, phone_gettable, account_creatable]).generate()
