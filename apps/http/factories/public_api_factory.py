from beanie import init_beanie
from fastapi import FastAPI

from apps.http.resources.news_resource import NewsResource
from apps.http.resources.base_resource import PublicGetRoutedAdder
from apps.http.resources.category_resource import CategoryResource
from common import MongoClientFactory
from config import API_DEBUG, GENERAL_MONGO_CONFIG
from models import auth
from .api_factory import APIFactory, APICreatable


class PublicAPIFactory(APICreatable):
    def __init__(self):
        routed = PublicGetRoutedAdder()
        self.__factory = APIFactory([NewsResource(routed=routed),
                                     CategoryResource(routed=routed)],
                                    name='Public resource',
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        app = self.__factory.create_app()

        @app.on_event('startup')
        async def collections_initialized():
            client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
            await init_beanie(
                getattr(client, GENERAL_MONGO_CONFIG['db']),
                document_models=[auth.News, auth.Category])

        return app
