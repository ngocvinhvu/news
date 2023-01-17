from datetime import datetime
from typing import (
    Optional)

from beanie import Indexed
from pydantic import Field
from pymongo import (
    TEXT,
    IndexModel,
    ASCENDING)

from ._based_document import BasedDocument


class Account(BasedDocument):
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    tenant_id: Indexed(str, unique=True)
    phone: Indexed(str, unique=True)
    email: Indexed(str, unique=True)

    password: str

    class Settings(BasedDocument.Settings):
        name = 'accounts'


class News(BasedDocument):
    html: str
    summary: str
    description: str
    image_url: str
    detail_url: str
    hash: Indexed(str, unique=True)
    generated_at: Indexed(datetime) = Field(default_factory=datetime.utcnow)

    category_id: Indexed(str) = None
    publisher_id: Indexed(str) = None

    class Settings(BasedDocument.Settings):
        name = 'news'

        indexes = [
            IndexModel([
                ('category_id', ASCENDING),
                ('publisher_id', ASCENDING),
            ], name='auth_news_ascending'),

            IndexModel([
                ('description', TEXT),
                ('summary', TEXT),
            ]),
        ]


class Publisher(BasedDocument):
    image_url: str = None
    summary: Indexed(str)
    description: Optional[str] = None

    class Settings(BasedDocument.Settings):
        name = 'publishers'


class PublisherCategory(BasedDocument):
    category_id: Indexed(str)
    publisher_id: Indexed(str)

    rss_url: str

    class Settings(BasedDocument.Settings):
        name = 'category_publisher'
        indexes = [
            IndexModel([
                ('category_id', ASCENDING),
                ('publisher_id', ASCENDING),
            ], name='auth_publisher_category_ascending')
        ]


class Category(BasedDocument):
    image_url: str = None
    summary: Indexed(str)
    description: Optional[str] = None

    class Settings(BasedDocument.Settings):
        name = 'categories'
