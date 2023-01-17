from abc import ABC, abstractmethod
from typing import List, Type

import inflect
from beanie import Document
from fastapi import (
    Depends,
    HTTPException)
from pydantic import BaseModel
from pymongo.client_session import ClientSession

from apps.http.requests import (
    GetRequest,
    DeleteRequest)
from common import MongoClientFactory
from config import GENERAL_MONGO_CONFIG
from services import (
    DocumentQueriedService,
    DocumentCreatableService,
    DocumentUpdatableService,
    DocumentDeletableService,
    AsyncModelQueryable,
    AsyncModelCreatable,
    AsyncModelUpdatable,
    AsyncModelDeletable,
    AuthenticationUser)
from .resource import Resource

p = inflect.engine()


class RoutedAddable(ABC):
    @abstractmethod
    def execute(self, path: str, resource: Resource):
        pass


class BaseResource(Resource):
    def __init__(self,
                 path: str = None,
                 mongo_config: dict = None,
                 routed: RoutedAddable = None):
        super(BaseResource, self).__init__()
        path = path or f'/{p.plural(self.create_document().__name__.lower())}'
        routed = routed or AuthRoutedAdder()
        routed.execute(path, self)

        self.__mongo_config = mongo_config or GENERAL_MONGO_CONFIG

    def create_document(self) -> Type[Document]:
        pass

    def create_project_document(self) -> Type[BaseModel] | None:
        return None

    def _create_queryable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelQueryable:
        return DocumentQueriedService(self.create_document(),
                                      projection_model=self.create_project_document(),
                                      session=session)

    def _create_creatable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        return DocumentCreatableService(self.create_document(), session=session)

    def _create_updatable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        return DocumentUpdatableService(self.create_document(), session=session)

    def _create_deletable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelDeletable:
        return DocumentDeletableService(self.create_document(), session=session)

    async def get(self, model_id: str | None = None,
                  request: GetRequest = Depends(GetRequest),
                  current_user=None):
        service = self._create_queryable(current_user=current_user, request=request)
        model_id = model_id or request.id

        if model_id:
            model = await service.get(model_id)
            if not model:
                raise HTTPException(404, {'message': 'Not found'})

            return model.dict()

        attributes = {'deleted': False, **request.filters}
        total = await service.count(attributes)

        models = await service.list(attributes,
                                    sorts=(request.sort, request.order),
                                    limit=request.limit,
                                    offset=request.offset)

        return {'items': [model.dict() for model in models],
                'meta': {'total': total,
                         'limit': request.limit,
                         'offset': request.offset}}

    async def post(self, payload: BaseModel | List[BaseModel],
                   request: GetRequest = Depends(GetRequest),
                   current_user=None):
        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)
        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_creatable(session=session,
                                                 request=request,
                                                 current_user=current_user)
                multitude = payload
                if not isinstance(payload, List):
                    multitude = [payload] if payload else []

                models = []
                for item in multitude:
                    model = await service.create(attributes=item.dict())
                    models.append(model.dict())

                return {'items': models,
                        'meta': {'total': len(models)}}

    async def patch(self, payload: BaseModel | List[BaseModel] = None,
                    request: GetRequest = Depends(GetRequest),
                    model_id: str | None = None,
                    current_user=None):
        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)
        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_updatable(session=session,
                                                 request=request,
                                                 current_user=current_user)
                if model_id:
                    payload = payload.dict() if payload else {}
                    await service.update(model_id, payload)
                    return {'_id': model_id}

                multitude = payload
                if not isinstance(payload, List):
                    multitude = [payload] if payload else []

                models = []
                for item in multitude:
                    await service.update(model_id, attributes=item.dict())
                    models.append({'_id': model_id})

                return {'items': models,
                        'meta': {'total': len(models)}}

    async def delete(self, payload: DeleteRequest | List[DeleteRequest] = None,
                     request: GetRequest = Depends(GetRequest),
                     model_id: str | None = None,
                     current_user=None):
        factory = MongoClientFactory()
        client = factory.create(self.__mongo_config)
        async with await client.start_session() as session:
            async with session.start_transaction():
                service = self._create_deletable(session=session,
                                                 current_user=current_user,
                                                 request=request)
                if model_id:
                    multitude = [model_id]

                else:
                    if not isinstance(payload, List):
                        multitude = [payload.id] if payload else []
                    else:
                        multitude = [item.id for item in payload]

                for item_id in multitude:
                    await service.delete(item_id)

                return None


class AuthRoutedAdder(RoutedAddable):

    def execute(self, path: str, resource: BaseResource):
        resource.router.add_api_route(path, resource.get, methods=['GET'], status_code=200)
        resource.router.add_api_route(path, resource.post, methods=['POST'], status_code=201)
        resource.router.add_api_route(path, resource.patch, methods=['PATCH'], status_code=200)
        resource.router.add_api_route(path, resource.delete, methods=['DELETE'], status_code=204)

        model_id = '{model_id}'
        resource.router.add_api_route(f'{path}/{model_id}', resource.get, methods=['GET'], status_code=200)
        resource.router.add_api_route(f'{path}/{model_id}', resource.patch, methods=['PATCH'], status_code=200)
        resource.router.add_api_route(f'{path}/{model_id}', resource.delete, methods=['DELETE'], status_code=204)


class PublicGetRoutedAdder(RoutedAddable):
    def execute(self, path: str, resource: BaseResource):
        resource.router.add_api_route(path, resource.get, methods=['GET'], status_code=200)

        model_id = '{model_id}'
        resource.router.add_api_route(f'{path}/{model_id}', resource.get, methods=['GET'], status_code=200)
