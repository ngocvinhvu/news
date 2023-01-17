import uvicorn

from apps.http.factories import AuthAPIFactory
from config import (
    AUTH_APP_PORT,
    AUTH_APP_HOST)

app = AuthAPIFactory().create_app()
uvicorn.run(app, port=AUTH_APP_PORT, host=AUTH_APP_HOST)

