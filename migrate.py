import asyncio
from logging import getLogger

from beanie import init_beanie
from pymongo.client_session import ClientSession

from common import (
    MongoClientFactory,
    GeneratedExecutor)
from config import GENERAL_MONGO_CONFIG
from models import *
from services import (
    RelatedGenerated,
    DocumentIndexGettable,
    AccountCreatable)

log = getLogger(__name__)


def create_account_generated(data: dict, index_field: str, session: ClientSession):
    account_gettable = DocumentIndexGettable(Account, {index_field: data[index_field]}, session=session)
    account_creatable = AccountCreatable(data, session=session)
    return GeneratedExecutor([account_gettable, account_creatable])


async def __init_data():
    client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
    async with await client.start_session() as mongo_session:
        async with mongo_session.start_transaction():
            account_service = create_account_generated({
                'email': 'admin@admin.com',
                'password': '123456',
                'phone': '0123456789'
            }, 'email', session=mongo_session)
            await account_service.generate()

            publisher = await RelatedGenerated(Publisher, {'summary': 'VnExpress'},
                                               session=mongo_session).generated_result()

            category_1 = await RelatedGenerated(Category, {'summary': 'Social'},
                                                session=mongo_session).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_1.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/thoi-su.rss'},
                                   session=mongo_session).generated_result()

            category_2 = await RelatedGenerated(Category, {'summary': 'Startup'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_2.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/startup.rss'},
                                   session=mongo_session).generated_result()

            category_3 = await RelatedGenerated(Category, {'summary': 'World'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_3.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/the-gioi.rss'},
                                   session=mongo_session).generated_result()

            category_4 = await RelatedGenerated(Category, {'summary': 'Business'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_4.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/kinh-doanh.rss'},
                                   session=mongo_session).generated_result()

            category_5 = await RelatedGenerated(Category, {'summary': 'Entertainment'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_5.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/giai-tri.rss'},
                                   session=mongo_session).generated_result()

            category_6 = await RelatedGenerated(Category, {'summary': 'Laws'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_6.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/phap-luat.rss'},
                                   session=mongo_session).generated_result()

            category_7 = await RelatedGenerated(Category, {'summary': 'Education'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_7.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/giao-duc.rss'},
                                   session=mongo_session).generated_result()

            category_8 = await RelatedGenerated(Category, {'summary': 'Health'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_8.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/suc-khoe.rss'},
                                   session=mongo_session).generated_result()

            category_9 = await RelatedGenerated(Category, {'summary': 'Family'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_9.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/gia-dinh.rss'},
                                   session=mongo_session).generated_result()

            category_10 = await RelatedGenerated(Category, {'summary': 'Travel'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_10.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/du-lich.rss'},
                                   session=mongo_session).generated_result()

            category_11 = await RelatedGenerated(Category, {'summary': 'Science'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_11.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/khoa-hoc.rss'},
                                   session=mongo_session).generated_result()

            category_12 = await RelatedGenerated(Category, {'summary': 'Vehicle'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_12.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/oto-xe-may.rss'},
                                   session=mongo_session).generated_result()

            category_13 = await RelatedGenerated(Category, {'summary': 'Community'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_13.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/thoi-su.rss'},
                                   session=mongo_session).generated_result()

            category_14 = await RelatedGenerated(Category, {'summary': 'Confession'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_14.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/tam-su.rss'},
                                   session=mongo_session).generated_result()

            category_15 = await RelatedGenerated(Category, {'summary': 'Comedy'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_15.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/cuoi.rss'},
                                   session=mongo_session).generated_result()

            category_16 = await RelatedGenerated(Category, {'summary': 'Sport'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_16.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/the-thao.rss'},
                                   session=mongo_session).generated_result()

            category_17 = await RelatedGenerated(Category, {'summary': 'Digital'}).generated_result()
            await RelatedGenerated(PublisherCategory, {'publisher_id': str(publisher.id),
                                                       'category_id': str(category_17.id), },
                                   data={'rss_url': 'https://vnexpress.net/rss/so-hoa.rss'},
                                   session=mongo_session).generated_result()


async def __run_migrate():
    client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
    await init_beanie(getattr(client, GENERAL_MONGO_CONFIG['db']),
                      document_models=[auth.Account, auth.News, auth.Publisher, auth.Category, auth.PublisherCategory])


def init_based_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__run_migrate())
    loop.run_until_complete(__init_data())
