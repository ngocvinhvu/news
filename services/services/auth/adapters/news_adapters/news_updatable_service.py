from hashlib import md5

from pymongo.client_session import ClientSession

from common import HandledGenerated
from models.auth import News
from services.common import AsyncModelUpdatable
from services.services.document_services import DocumentIndexGettable
from .news_creatable_service import DuplicatedNewsHandler


class NewsUpdatableService(AsyncModelUpdatable):
    def __init__(self, updatable: AsyncModelUpdatable,
                 session: ClientSession = None):
        self.__session = session
        self.__updatable = updatable

    async def update(self, model_id: str, attributes: dict, **kwargs):
        hash_str = str(attributes['summary'] + attributes['description'])
        attributes['hash'] = md5(hash_str.encode()).hexdigest()

        news_gettable = DocumentIndexGettable(News, {'hash': attributes['hash']}, session=self.__session,
                                              executed_services=[HandledGenerated(
                                                  DuplicatedNewsHandler('news', attributes['summary']))])

        return await self.__updatable.update(model_id, attributes, pre_generated_services=[news_gettable])
