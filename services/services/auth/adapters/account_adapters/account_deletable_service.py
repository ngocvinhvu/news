from beanie.odm.fields import PydanticObjectId
from pymongo.client_session import ClientSession

from common import (
    GeneratedExecutor)
from services.common import AsyncModelDeletable
from services.services.auth.generated import (
    AccountIndexGettable,
    AccountDeletable)


class AccountDeletableService(AsyncModelDeletable):

    def __init__(self, session: ClientSession = None):
        self.__session = session

    async def delete(self, model_id: str, **kwargs):
        account_gettable = AccountIndexGettable({'_id': PydanticObjectId(model_id)}, session=self.__session)
        account_deletable = AccountDeletable(session=self.__session)
        return await GeneratedExecutor([account_gettable, account_deletable]).generate()
