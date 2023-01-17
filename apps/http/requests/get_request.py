import json
import re

from beanie.odm.fields import SortDirection

from constants import VI_LOCALE


class GetRequest:
    def __init__(self,
                 id: str = None,
                 offset: int = 0,
                 limit: int = 100,
                 q: str | None = None,
                 filters: str = None,
                 sort: str | None = None):
        self.q = q
        self.id = id
        self.sort = 'created'
        self.order = SortDirection.ASCENDING
        self.limit = limit
        self.offset = offset

        if sort:
            mapping = {
                '+': SortDirection.ASCENDING,
                '-': SortDirection.DESCENDING
            }

            match = re.search(r'([-+]?)([_\w]+)', sort)
            sort_str = match.group(2)
            order_indicator = match.group(1)

            self.sort = sort_str or 'created'
            self.order = mapping.get(order_indicator, SortDirection.ASCENDING)

        try:
            filters = filters or '{}'
            self.filters: dict = json.loads(filters.replace("'", "\""))
        except json.JSONDecodeError:
            raise ValueError(f'Invalid filters params')

        self._update()

    def _update(self):
        return True


class ManagementGetRequest(GetRequest):
    def __init__(self,
                 id: str = None,
                 offset: int = 0,
                 limit: int = 100,
                 filters: str = None,
                 q: str | None = None,
                 locale: str = VI_LOCALE,
                 sort: str | None = None):
        super(ManagementGetRequest, self).__init__(id=id,
                                                   filters=filters,
                                                   offset=offset,
                                                   limit=limit,
                                                   sort=sort,
                                                   q=q)
        self.locale = locale
