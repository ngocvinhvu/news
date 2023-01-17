from .account_resource import AccountResource
from .category_resource import CategoryResource
from .login import LoginResource
from .news_resource import NewsResource
from .publisher_resource import PublisherResource

resources = [
    LoginResource(),
    AccountResource(),
    NewsResource(),
    PublisherResource(),
    CategoryResource(),
]
