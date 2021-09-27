from .encoders import jsonable_encoder
from .exceptions import RequestValidationError, HTTPException

# from starlette.exceptions import HTTPException
# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from http import HTTPStatus

HTTP_422_UNPROCESSABLE_ENTITY = int(HTTPStatus.UNPROCESSABLE_ENTITY)

from ..base import Request, JSONResponse


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(
            {"detail": exc.detail}, status=exc.status_code, headers=headers
        )
    else:
        return JSONResponse({"detail": exc.detail}, status=exc.status_code)


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status=HTTP_422_UNPROCESSABLE_ENTITY,
        data={"detail": jsonable_encoder(exc.errors())},
    )
