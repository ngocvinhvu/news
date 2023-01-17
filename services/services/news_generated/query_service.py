from typing import Any

from pymongo.client_session import ClientSession

from common import (
    AsyncGenerated,
    GeneratedExecutor,
    AsyncResultGenerated)
from services.common import (
    NewsExecutable,
    NewsIn)
from services.exceptions import UniqueException
from services.services.auth import NewsCreatableService
from services.services.document_services import (
    DocumentCreatable,
    DocumentIndexGettable)
from logging import getLogger

log = getLogger(__name__)


class QueryGenerated(AsyncGenerated):
    def __init__(self, http_generated: AsyncGenerated, executable: NewsExecutable):

        self.__executable = executable
        self.__http_generated = http_generated

    async def generate(self) -> Any:
        raw = await self.__http_generated.generate()
        generators = self.__executable.execute(raw)
        total_generator = len(generators)

        log.info('Total query results: %s', total_generator)
        count = 0

        for generated in generators:
            count += 1
            try:
                log.info('%s/%s. Insert news.', count, total_generator)
                await generated.generate()
            except UniqueException:
                log.debug('Duplicated news. Skip insert')
                continue


class NewsCreatableGenerated(AsyncResultGenerated):
    def __init__(self, news: NewsIn, session: ClientSession = None):
        self.__news = news
        self.__service = NewsCreatableService(session=session)

    async def generated_result(self, result: Any = None) -> Any:
        return await self.__service.create(self.__news.dict())


class RelatedGenerated(AsyncResultGenerated):
    def __init__(self, _type, filters: dict,
                 data: dict = None,
                 session: ClientSession = None):
        self.__data = data
        self.__type = _type
        self.__session = session
        self.__filters = filters

    async def generated_result(self, result: Any = None) -> Any:
        gettable = DocumentIndexGettable(self.__type, self.__filters, session=self.__session)
        creatable = DocumentCreatable(self.__type, session=self.__session,
                                      attributes={**(self.__data or {}), **self.__filters})
        return await GeneratedExecutor([gettable, creatable]).generate()
