from fastapi import APIRouter, Header

from services.services.auth import (
    AccountTokenDecodedService)


class Resource:
    def __init__(self):
        self.router = APIRouter()


def authenticate_admin(authorization=Header(...)):
    decoded_service = AccountTokenDecodedService(authorization)
    return decoded_service.generate()
