from typing import Type

from beanie import Document
from fastapi import Depends

from apps.http.requests import GetRequest
from apps.http.resources.base_resource import BaseResource
from models.auth import Category


class CategoryResource(BaseResource):

    def create_document(self) -> Type[Document]:
        return Category

    async def get(self, model_id: str | None = None,
                  current_user=None,
                  request: GetRequest = Depends(GetRequest)):
        return await super(CategoryResource, self).get(request=request,
                                                       model_id=model_id,
                                                       current_user=current_user)
