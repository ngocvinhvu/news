from services.common import (
    AsyncModelDeletable,
    AsyncModelUpdatable)


class NewsDeletableService(AsyncModelDeletable):
    def __init__(self, updatable: AsyncModelUpdatable):
        self.__updatable = updatable

    async def delete(self, model_id: str, **kwargs):
        return await self.__updatable.update(model_id, attributes={'deleted': True})



