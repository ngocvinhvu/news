from beanie.odm.fields import PydanticObjectId
from pymongo.client_session import ClientSession

from common import (
    GeneratedExecutor,
    HandledGenerated)
from models.auth import Account
from services.common import AsyncModelUpdatable
from services.services.auth.generated import (
    AccountIndexGettable,
    AccountUpdatable)
from .account_creatable_service import DuplicatedEmailHandler


class AccountUpdatableService(AsyncModelUpdatable):

    def __init__(self, session: ClientSession = None):
        self.__session = session

    async def update(self, model_id: str, attributes: dict, **kwargs) -> Account:
        email = attributes.get('email')
        phone = attributes.get('phone')

        generators = []
        if email:
            email_gettable = AccountIndexGettable({'email': email},
                                                  session=self.__session,
                                                  executed_services=[HandledGenerated(
                                                      DuplicatedEmailHandler('email', email))])
            generators.append(email_gettable)
        if phone:
            phone_gettable = AccountIndexGettable({'phone': phone},
                                                  session=self.__session,
                                                  executed_services=[HandledGenerated(
                                                      DuplicatedEmailHandler('phone number', phone))])
            generators.append(phone_gettable)

        generators.append(AccountIndexGettable({'_id': PydanticObjectId(model_id)}, session=self.__session))
        generators.append(AccountUpdatable(attributes, session=self.__session))
        return await GeneratedExecutor(generators).generate()
