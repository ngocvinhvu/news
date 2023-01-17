from datetime import datetime
from typing import Type

from beanie import Document
from fastapi import Depends
from pydantic import (
    BaseModel)

from apps.http.requests import (
    GetRequest)
from apps.http.resources.base_resource import BaseResource
from models.auth import News


class NewsOut(BaseModel):
    html: str
    summary: str
    image_url: str
    detail_url: str
    description: str
    generated_at: datetime


class NewsGetRequest(GetRequest):
    def _update(self):
        if self.q:
            self.filters = {
                '$text':
                    {
                        '$search': self.q,
                        '$language': 'en',
                        '$caseSensitive': False,
                        '$diacriticSensitive': False
                    }, **self.filters
            }


class NewsResource(BaseResource):

    def create_document(self) -> Type[Document]:
        return News

    def create_project_document(self) -> Type[BaseModel] | None:
        return NewsOut

    async def get(self, model_id: str | None = None,
                  current_user=None,
                  request: NewsGetRequest = Depends(NewsGetRequest)):
        return await super(NewsResource, self).get(request=request,
                                                   model_id=model_id,
                                                   current_user=current_user)
