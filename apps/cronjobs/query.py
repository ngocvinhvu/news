import asyncio
import time
from logging import getLogger

import schedule
from beanie import init_beanie

from common import (
    MongoClientFactory)
from config import GENERAL_MONGO_CONFIG
from models import *
from services import (
    QueryGenerated,
    VNExpressGenerated,
    AIOHttpGenerated)

log = getLogger(__name__)


def job_execute():
    schedule.every(10).minutes.do(query_news_data)

    log.info('Cronjob is running')
    while True:
        schedule.run_pending()
        time.sleep(1)


def query_news_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__run_migrate())
    loop.run_until_complete(__query_data())


async def __run_migrate():
    client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
    await init_beanie(getattr(client, GENERAL_MONGO_CONFIG['db']),
                      document_models=[auth.Account, auth.News, auth.Publisher, auth.Category, auth.PublisherCategory])


async def __query_data():
    results = await PublisherCategory.find_many().to_list()
    for result in results:
        client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
        async with await client.start_session() as mongo_session:
            async with mongo_session.start_transaction():
                generated = QueryGenerated(AIOHttpGenerated(result.rss_url),
                                           VNExpressGenerated(result.category_id, result.publisher_id,
                                                              session=mongo_session))

                await generated.generate()
