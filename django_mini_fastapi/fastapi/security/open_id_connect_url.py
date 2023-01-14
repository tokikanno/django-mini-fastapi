from typing import Optional
from http import HTTPStatus


from ..openapi.models import OpenIdConnect as OpenIdConnectModel
from ..security.base import SecurityBase
from ...utils import get_http_header

# from starlette.exceptions import HTTPException
# from starlette.requests import Request
# from starlette.status import HTTP_403_FORBIDDEN

from ..exceptions import HTTPException
from ...base import Request

HTTP_401_UNAUTHORIZED = int(HTTPStatus.UNAUTHORIZED)
HTTP_403_FORBIDDEN = int(HTTPStatus.FORBIDDEN)


class OpenIdConnect(SecurityBase):
    def __init__(
        self,
        *,
        openIdConnectUrl: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True
    ):
        self.model = OpenIdConnectModel(
            openIdConnectUrl=openIdConnectUrl, description=description
        )
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    def __call__(self, request: Request) -> Optional[str]:
        authorization = get_http_header(request.META, "Authorization")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return authorization
