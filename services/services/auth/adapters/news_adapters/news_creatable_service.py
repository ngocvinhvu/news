from hashlib import md5

from pymongo.client_session import ClientSession

from common import (
    GeneratedExecutor,
    HandledGenerated,
    ResultGenerated)
from models.auth import News
from services.common import AsyncModelCreatable
from services.exceptions import UniqueException
from services.services.document_services import (
    DocumentIndexGettable,
    DocumentCreatable)


class DuplicatedNewsHandler(ResultGenerated):
    def __init__(self, key: str, value: str):
        self.__key = key
        self.__value = value

    def generated_result(self, news: News | None) -> News | None:
        if news:
            raise UniqueException(f'Existed {self.__key}: {self.__value}')

        return news


class NewsCreatableService(AsyncModelCreatable):
    def __init__(self, session: ClientSession = None):
        self.__session = session

    async def create(self, attributes: dict, **kwargs) -> News:
        hash_str = str(attributes['summary'] + attributes['description'])
        attributes['hash'] = md5(hash_str.encode()).hexdigest()

        news_gettable = DocumentIndexGettable(News, {'hash': attributes['hash']}, session=self.__session,
                                              executed_services=[HandledGenerated(
                                                  DuplicatedNewsHandler('news', attributes['summary']))])
        news_creatable = DocumentCreatable(News, session=self.__session, attributes=attributes)

        return await GeneratedExecutor([news_gettable, news_creatable]).generate()
