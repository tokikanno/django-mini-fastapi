from typing import Any, Callable, Iterable, Type
from django.http import (
    HttpRequest as Request,
    HttpResponse as Response,
    JsonResponse,
)
from django.core.files.uploadedfile import UploadedFile


class JSONResponse(JsonResponse):
    media_type = "application/json"


class HTMLResponse(Response):
    media_type = "text/html"


class TempResponse(Response):
    def __init__(self) -> None:
        super().__init__()
        # set empty status_code
        self.status_code = None


class UploadFile(UploadedFile):
    @classmethod
    def __get_validators__(cls: Type["UploadFile"]) -> Iterable[Callable[..., Any]]:
        yield cls.validate

    @classmethod
    def validate(cls: Type["UploadFile"], v: Any) -> Any:
        if not isinstance(v, UploadedFile):
            raise ValueError(f"Expected UploadedFile, received: {type(v)}")
        return v
