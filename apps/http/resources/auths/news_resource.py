from typing import Type, List

from beanie import Document
from fastapi import Depends
from pydantic import (
    BaseModel)
from pymongo.client_session import ClientSession

from apps.http.requests import (
    DeleteRequest,
    GetRequest)
from apps.http.resources.base_resource import BaseResource
from apps.http.resources.resource import authenticate_admin
from services import (
    NewsCreatableService,
    AsyncModelCreatable,
    AuthenticationUser,
    AsyncModelUpdatable,
    NewsUpdatableService,
    AsyncModelDeletable,
    NewsDeletableService)
from models.auth import News


class NewsIn(BaseModel):
    summary: str
    image_url: str
    detail_url: str
    description: str
    html: str
    category_id: str
    publisher_id: str


class NewsResource(BaseResource):
    def create_document(self) -> Type[Document]:
        return News

    def _create_creatable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelCreatable:
        return NewsCreatableService(session)

    def _create_updatable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelUpdatable:
        updatable = super()._create_updatable(session=session, current_user=current_user, request=request, **kwargs)
        return NewsUpdatableService(updatable, session=session)

    def _create_deletable(self, session: ClientSession | None = None,
                          current_user: AuthenticationUser = None,
                          request: GetRequest = None,
                          **kwargs) -> AsyncModelDeletable:
        updatable = super()._create_updatable(session=session, current_user=current_user, request=request, **kwargs)
        return NewsDeletableService(updatable)

    async def get(self, model_id: str | None = None,
                  current_user=Depends(authenticate_admin),
                  request: GetRequest = Depends(GetRequest)):
        return await super(NewsResource, self).get(request=request,
                                                   model_id=model_id,
                                                   current_user=current_user)

    async def post(self, payload: NewsIn | List[NewsIn],
                   request: GetRequest = Depends(GetRequest),
                   current_user=None):
        return await super(NewsResource, self).post(payload, current_user=current_user)

    async def patch(self, payload: NewsIn | List[NewsIn] = None,
                    current_user=Depends(authenticate_admin),
                    request: GetRequest = Depends(GetRequest),
                    model_id: str | None = None):
        return await super(NewsResource, self).patch(payload=payload,
                                                     request=request,
                                                     model_id=model_id,
                                                     current_user=current_user)

    async def delete(self, payload: DeleteRequest | List[DeleteRequest] = None,
                     current_user=Depends(authenticate_admin),
                     request: GetRequest = Depends(GetRequest),
                     model_id: str | None = None):
        return await super(NewsResource, self).delete(payload=payload,
                                                      request=request,
                                                      model_id=model_id,
                                                      current_user=current_user)
