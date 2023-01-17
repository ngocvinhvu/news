import uvicorn

from apps.http.factories import PublicAPIFactory
from config import (
    MANAGEMENT_APP_PORT,
    MANAGEMENT_APP_HOST)

app = PublicAPIFactory().create_app()
uvicorn.run(app, port=MANAGEMENT_APP_PORT, host=MANAGEMENT_APP_HOST)

