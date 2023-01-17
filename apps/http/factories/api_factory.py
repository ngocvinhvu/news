from abc import (ABC, abstractmethod)
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.http.exceptions import MethodNotAllowException
from apps.http.resources import Resource
from exceptions import ServiceException
from services.exceptions import (
    UniqueException,
    NotFoundException,
    UnauthorizedException)
from config import CORS_ORIGINS


async def method_not_allow_handler(_, __):
    return JSONResponse({'message': 'Method not allowed'}, status_code=405)


async def value_error_handler(_, __):
    return JSONResponse({'message': 'Bad request'}, status_code=400)


async def unique_error_handler(_, exception):
    return JSONResponse({'message': str(exception)}, status_code=403)


async def not_found_error_handler(_, __):
    return JSONResponse({'message': 'Not found'}, status_code=404)


async def unauthorized_error_handler(_, exception):
    message = str(exception) or 'Unauthorized'
    return JSONResponse({'message': message}, status_code=401)


async def default_error_handler(_, exception: ServiceException):
    return JSONResponse({'message': str(exception)}, status_code=exception.get_code())


class APICreatable(ABC):
    @abstractmethod
    def create_app(self) -> FastAPI:
        pass


class APIFactory(APICreatable):
    def __init__(self, routes: List[Resource],
                 name: str = None,
                 debug: bool = None,
                 prefix: str = None,
                 description: str = None):
        self.__name = name
        self.__routes = routes
        self.__debug = debug or False
        self.__prefix = prefix
        self.__description = description

    def create_app(self) -> FastAPI:
        app = FastAPI(title=self.__name,
                      debug=self.__debug,
                      description=self.__description,
                      root_path=self.__prefix)

        for resource in self.__routes:
            app.include_router(resource.router)

        app.add_exception_handler(MethodNotAllowException, method_not_allow_handler)
        app.add_exception_handler(UnauthorizedException, unauthorized_error_handler)
        app.add_exception_handler(NotFoundException, not_found_error_handler)
        app.add_exception_handler(UniqueException, unique_error_handler)
        app.add_exception_handler(ServiceException, default_error_handler)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        if not self.__debug:
            app.add_exception_handler(ValueError, value_error_handler)

        return app
