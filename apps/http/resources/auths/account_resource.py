from datetime import datetime
from typing import Type, List, Optional

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from fastapi import Depends
from pydantic import (
    BaseModel,
    Field)
from pymongo.client_session import ClientSession

from apps.http.requests import (
    DeleteRequest,
    GetRequest)
from apps.http.resources.base_resource import BaseResource
from apps.http.resources.resource import authenticate_admin
from models.auth import Account
from services import (
    AccountCreatableService,
    AccountDeletableService,
    AccountUpdatableService,
    AsyncModelCreatable,
    AsyncModelDeletable,
    AsyncModelUpdatable)


class AccountIn(BaseModel):
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password: str
    email: str
    phone: str


class AccountUpdate(BaseModel):
    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    password: Optional[str]
    phone: Optional[str]


class AccountOut(BaseModel):
    # Filter password on out
    id: Optional[PydanticObjectId] = Field(alias='_id')
    created: datetime
    updated: datetime

    avatar_url: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: str
    phone: str


class AccountResource(BaseResource):
    def create_document(self) -> Type[Document]:
        return Account

    def create_project_document(self) -> Type[BaseModel] | None:
        return AccountOut

    def _create_creatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelCreatable:
        return AccountCreatableService(session=session)

    def _create_deletable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelDeletable:
        return AccountDeletableService(session)

    def _create_updatable(self, session: ClientSession | None = None, **kwargs) -> AsyncModelUpdatable:
        return AccountUpdatableService(session)

    async def get(self, model_id: str | None = None,
                  current_user=Depends(authenticate_admin),
                  request: GetRequest = Depends(GetRequest)):
        return await super(AccountResource, self).get(request=request,
                                                      model_id=model_id,
                                                      current_user=current_user)

    async def post(self, payload: AccountIn | List[AccountIn],
                   request: GetRequest = Depends(GetRequest),
                   current_user=None):
        return await super(AccountResource, self).post(payload, current_user=current_user)

    async def patch(self, payload: AccountUpdate | List[AccountUpdate] = None,
                    current_user=Depends(authenticate_admin),
                    request: GetRequest = Depends(GetRequest),
                    model_id: str | None = None):
        return await super(AccountResource, self).patch(payload=payload,
                                                        request=request,
                                                        model_id=model_id,
                                                        current_user=current_user)

    async def delete(self, payload: DeleteRequest | List[DeleteRequest] = None,
                     current_user=Depends(authenticate_admin),
                     request: GetRequest = Depends(GetRequest),
                     model_id: str | None = None):
        return await super(AccountResource, self).delete(payload=payload,
                                                         request=request,
                                                         model_id=model_id,
                                                         current_user=current_user)
