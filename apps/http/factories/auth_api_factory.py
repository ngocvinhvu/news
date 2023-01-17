from beanie import init_beanie
from fastapi import FastAPI

from apps.http.resources.auths import resources as auth_resources
from common import MongoClientFactory
from config import API_DEBUG, GENERAL_MONGO_CONFIG
from models import auth
from .api_factory import APIFactory, APICreatable


class AuthAPIFactory(APICreatable):
    def __init__(self):
        self.__factory = APIFactory(auth_resources,
                                    name='Auth resource',
                                    debug=API_DEBUG)

    def create_app(self) -> FastAPI:
        app = self.__factory.create_app()

        @app.on_event('startup')
        async def collections_initialized():
            client = MongoClientFactory().create(GENERAL_MONGO_CONFIG)
            await init_beanie(
                getattr(client, GENERAL_MONGO_CONFIG['db']),
                document_models=[auth.Account, auth.News, auth.Category, auth.Publisher, auth.PublisherCategory])

        return app
