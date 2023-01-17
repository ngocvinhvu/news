from typing import Type, List

from beanie import Document
from fastapi import Depends
from pydantic import (
    BaseModel)

from apps.http.requests import (
    DeleteRequest,
    GetRequest)
from apps.http.resources.base_resource import BaseResource
from apps.http.resources.resource import authenticate_admin
from models.auth import PublisherCategory


class PublisherCategoryIn(BaseModel):
    publisher_id: str
    category_id: str
    rss_url: str = None


class PublisherResource(BaseResource):
    def create_document(self) -> Type[Document]:
        return PublisherCategory

    async def get(self, model_id: str | None = None,
                  current_user=Depends(authenticate_admin),
                  request: GetRequest = Depends(GetRequest)):
        return await super(PublisherResource, self).get(request=request,
                                                        model_id=model_id,
                                                        current_user=current_user)

    async def post(self, payload: PublisherCategoryIn | List[PublisherCategoryIn],
                   request: GetRequest = Depends(GetRequest),
                   current_user=None):
        return await super(PublisherResource, self).post(payload, current_user=current_user)

    async def patch(self, payload: PublisherCategoryIn | List[PublisherCategoryIn] = None,
                    current_user=Depends(authenticate_admin),
                    request: GetRequest = Depends(GetRequest),
                    model_id: str | None = None):
        return await super(PublisherResource, self).patch(payload=payload,
                                                          request=request,
                                                          model_id=model_id,
                                                          current_user=current_user)

    async def delete(self, payload: DeleteRequest | List[DeleteRequest] = None,
                     current_user=Depends(authenticate_admin),
                     request: GetRequest = Depends(GetRequest),
                     model_id: str | None = None):
        return await super(PublisherResource, self).delete(payload=payload,
                                                           request=request,
                                                           model_id=model_id,
                                                           current_user=current_user)
