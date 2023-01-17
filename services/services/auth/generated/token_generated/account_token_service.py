from datetime import datetime, timedelta
from hashlib import md5
from typing import List

from jose import jwt, JWTError
from pydantic import (
    BaseModel,
    ValidationError)
from pymongo.client_session import ClientSession

from common import (
    Generated,
    AsyncGenerated,
    HandledGenerated,
    ResultGenerated)
from config import (
    SECRET_KEY,
    EXPIRED_TIME)
from constants import ADMIN_PRIORITY
from models.auth import Account
from services.exceptions import UnauthorizedException
from services.services.auth.generated.account_generated import AccountIndexGettable


class AuthenticatedOrganization(BaseModel):
    id: str
    priority: int
    roles: List[str] = []


class AuthenticationUser(BaseModel):
    id: str
    organizations: List[AuthenticatedOrganization] = []


class AuthenticatedHandler(ResultGenerated):
    def __init__(self, password: str):
        self.__password = password

    def generated_result(self, account: Account | None) -> Account | None:
        if account:
            hashed = md5(self.__password.encode()).hexdigest()
            if hashed != account.password:
                raise UnauthorizedException('Invalid password')

            return account

        raise UnauthorizedException('Invalid email or password')


class AccountTokenService(AsyncGenerated):
    def __init__(self, email: str, password: str,
                 session: ClientSession = None):
        self.__email = email
        self.__session = session
        self.__password = password

    async def generate(self) -> str:
        account_gettable = AccountIndexGettable({'email': self.__email},
                                                session=self.__session,
                                                executed_services=[
                                                    HandledGenerated(AuthenticatedHandler(self.__password))])
        account = await account_gettable.generate()

        auth_account = AuthenticationUser(**{'id': str(account.id)})

        encoded_data = {
            **auth_account.dict(),
            'exp': datetime.utcnow() + timedelta(minutes=EXPIRED_TIME)
        }
        return jwt.encode(encoded_data, SECRET_KEY, algorithm='HS256')


class AccountTokenDecodedService(Generated):
    def __init__(self, token: str, session: ClientSession = None):
        self.__token = token
        self.__session = session

    def generate(self) -> AuthenticationUser:
        try:
            payload = jwt.decode(self.__token, SECRET_KEY, algorithms=['HS256'])
            auth_account = AuthenticationUser(**payload)
            return auth_account
        except JWTError:
            raise UnauthorizedException('Invalid token')

        except ValidationError:
            raise UnauthorizedException('Deprecated token')


class OrganizationDecodedService(Generated):
    def __init__(self, decoded_generated: Generated, organization_id: str):
        self.__organization_id = organization_id
        self.__decoded_generated = decoded_generated

    def generate(self) -> AuthenticationUser:
        auth = self.__decoded_generated.generate()
        for organization in auth.organizations:
            if organization.id == self.__organization_id or organization.priority == ADMIN_PRIORITY:
                return auth

        raise UnauthorizedException()


class AdminTokenDecodedService(Generated):
    def __init__(self, decoded_generated: Generated):
        self.__decoded_generated = decoded_generated

    def generate(self) -> AuthenticationUser:
        auth = self.__decoded_generated.generate()
        for organization in auth.organizations:
            if organization.priority == ADMIN_PRIORITY:
                return auth

        raise UnauthorizedException()
