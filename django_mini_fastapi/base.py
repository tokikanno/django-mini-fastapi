from typing import Any, Callable, Iterable, Type
from django.http import (
    HttpRequest as Request,
    HttpResponse as Response,
    JsonResponse,
)
from django.core.files.uploadedfile import UploadedFile

try:
    from django.http.request import HttpHeaders as Headers
except ImportError:
    Headers = dict
from django.http.request import QueryDict as QueryParams
from django.http.request import QueryDict as FormData
from django.contrib.sessions.backends.base import SessionBase as Session


class JSONResponse(JsonResponse):
    media_type = "application/json"


class HTMLResponse(Response):
    media_type = "text/html"


class TempResponse(Response):
    def __init__(self) -> None:
        super().__init__()
        # set empty status_code
        self.status_code = None

        # reset headers
        for k in ("headers", "_headers"):
            headers = getattr(self, k, None)
            if headers:
                setattr(self, k, headers.__class__({}))


class UploadFile(UploadedFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], v: Any) -> Any:
        if not isinstance(v, UploadedFile):
            raise ValueError(f"Expected UploadedFile, received: {type(v)}")
        return v
