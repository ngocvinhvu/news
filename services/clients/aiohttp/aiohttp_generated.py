from json import dumps, loads

import aiohttp
from xmltodict import parse

from common import AsyncGenerated
from exceptions import ServiceException


class AIOHttpGenerated(AsyncGenerated):
    def __init__(self, url: str):
        self.__url = url

    async def generate(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__url) as response:
                if response.status != 200:
                    raise ServiceException(f'RSS service unavailable: {self.__url}', code=503)

                return loads(dumps(parse(await response.text())))
