from typing import List

from html_to_json import convert
from pymongo.client_session import ClientSession
from dateutil import parser
from common import (
    AsyncGenerated,
    AsyncHandledGenerated)
from services.common import (
    NewsExecutable,
    NewsIn)
from .query_service import (
    NewsCreatableGenerated)
from datetime import timezone


class VNExpressGenerated(NewsExecutable):
    def __init__(self, category_id: str, publisher_id: str,
                 session: ClientSession = None):
        self.__category_id = category_id
        self.__publisher_id = publisher_id
        self.__session = session

    def execute(self, raw: dict) -> List[AsyncGenerated]:
        generated = []
        try:
            raw_items = raw['rss']['channel']['item']
        except KeyError:
            return generated

        for item in raw_items:
            detail = convert(item['description'])
            try:
                image_url = detail['a'][0]['img'][0]['_attributes']['src']
            except KeyError:
                image_url = ''

            news_creatable = NewsCreatableGenerated(NewsIn(**{
                'image_url': image_url,
                'summary': item['title'],
                'detail_url': item['link'],
                'html': item['description'],
                'description': detail['_value'],
                'category_id': self.__category_id,
                'publisher_id': self.__publisher_id,
                'generated_at': parser.parse(item['pubDate']).astimezone(timezone.utc)
            }))

            generated.append(AsyncHandledGenerated(news_creatable, result=1))

        return generated
