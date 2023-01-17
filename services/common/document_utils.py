from abc import ABC, abstractmethod


class AsyncModelGettable(ABC):
    @abstractmethod
    async def get(self, model_id: str, **kwargs):
        pass


class AsyncModelListable(ABC):
    @abstractmethod
    async def list(self, attributes: dict, **kwargs):
        pass


class AsyncModelCreatable(ABC):
    @abstractmethod
    async def create(self, attributes: dict, **kwargs):
        pass


class AsyncModelUpdatable(ABC):
    @abstractmethod
    async def update(self, model_id: str, attributes: dict, **kwargs):
        pass


class AsyncModelDeletable(ABC):
    @abstractmethod
    async def delete(self, model_id: str, **kwargs):
        pass


class AsyncModelExecutable(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass
