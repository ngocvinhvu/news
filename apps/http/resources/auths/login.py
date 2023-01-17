from pydantic import BaseModel

from apps.http.resources.resource import Resource
from services import AccountTokenService


class Auth(BaseModel):
    password: str
    email: str


class LoginResource(Resource):
    def __init__(self):
        super(LoginResource, self).__init__()
        self.router.add_api_route('/login', self.login, methods=['POST'])

    @staticmethod
    async def login(auth: Auth):
        token_service = AccountTokenService(auth.email, auth.password)
        return {'access_token': await token_service.generate(), 'token_type': 'bearer'}
