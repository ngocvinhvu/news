from motor.motor_asyncio import AsyncIOMotorClient

from .singleton import Singleton


class MongoClientFactory(metaclass=Singleton):
    def __init__(self):
        self.__clients = {}

    def create(self, config: dict) -> AsyncIOMotorClient:
        config_ident = config['hash']
        client = self.__clients.get(config_ident)
        if not client:
            client = AsyncIOMotorClient(config['uri'])
            self.__clients[config_ident] = client

        return client

