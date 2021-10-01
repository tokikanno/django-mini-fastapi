from typing import Any, Callable, Coroutine, Dict, List, Optional, Sequence, Type, Union

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponseNotAllowed

from .fastapi import FastAPI
from .fastapi.params import Depends
from .fastapi.exceptions import HTTPException
from .fastapi.datastructures import Default
from .base import HTMLResponse, Request, Response, JSONResponse
from .route import BaseRoute

import logging

_logger = logging.getLogger(__name__)


RAPIDOC_PAGE_TPL = """
<!doctype html> <!-- Important: must specify -->
<html>
<head>
<title>{title} - RapiDoc</title>
<meta charset="utf-8"> <!-- Important: rapi-doc uses utf8 charecters -->
<script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
</head>
<body>
<rapi-doc
    spec-url="{openapi_url}"
    sort-endpoints-by="method"
    render-style="read"
> </rapi-doc>
</body>
</html>
"""


class OpenAPI(FastAPI):
    def __init__(
        self,
        *,
        debug: bool = False,
        routes: Optional[List[BaseRoute]] = None,
        title: str = "Django mini FastAPI",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        rapidoc_url: Optional[str] = "/rapidoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
        exception_handlers: Optional[
            Dict[
                Union[int, Type[Exception]],
                Callable[[Request, Any], Coroutine[Any, Any, Response]],
            ]
        ] = None,
        terms_of_service: Optional[str] = None,
        contact: Optional[Dict[str, Union[str, Any]]] = None,
        license_info: Optional[Dict[str, Union[str, Any]]] = None,
        root_path: str = "",
        root_path_in_servers: bool = True,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        **extra: Any
    ) -> None:
        super().__init__(
            debug=debug,
            routes=routes,
            title=title,
            description=description,
            version=version,
            openapi_url=openapi_url,
            openapi_tags=openapi_tags,
            servers=servers,
            dependencies=dependencies,
            default_response_class=default_response_class,
            docs_url=docs_url,
            redoc_url=redoc_url,
            swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
            swagger_ui_init_oauth=swagger_ui_init_oauth,
            exception_handlers=exception_handlers,
            terms_of_service=terms_of_service,
            contact=contact,
            license_info=license_info,
            root_path=root_path,
            root_path_in_servers=root_path_in_servers,
            responses=responses,
            callbacks=callbacks,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
            **extra
        )

        self.rapidoc_url = rapidoc_url

        if self.openapi_url and self.rapidoc_url:

            def rapi_doc_html(req: Request) -> HTMLResponse:
                root_path = self.root_path.rstrip("/")
                openapi_url = root_path + self.openapi_url

                return HTMLResponse(
                    RAPIDOC_PAGE_TPL.format(title=self.title, openapi_url=openapi_url)
                )

            self.add_route(self.rapidoc_url, rapi_doc_html, include_in_schema=False)

    def as_django_url_pattern(self):
        return url(
            "^{prefix_path}/(?P<route_path>.*)".format(
                prefix_path=self.root_path.strip("/")
            ),
            self.as_django_view(),
        )

    def as_django_view(self):
        @csrf_exempt
        def dispatcher(request: Request, route_path: str):
            route_path = self.root_path + "/" + route_path.strip("/")

            matched_route = None
            matched_route_path_kwargs = None
            method_not_allowed_routes: List[BaseRoute] = []

            try:
                for route in self.router.routes:
                    path_kwargs: Optional[Dict[str, str]] = route.match_path(route_path)

                    # path regex not matched
                    if path_kwargs is None:
                        continue

                    # found 1st full matched route, break here
                    if route.check_method_allowed(request.method):
                        matched_route = route
                        matched_route_path_kwargs = path_kwargs
                        break
                    else:
                        method_not_allowed_routes.append(route)
                else:
                    # no break after scanned all routes
                    if method_not_allowed_routes:
                        raise HTTPException(405)
                    else:
                        raise HTTPException(404)

                request.path_kwargs = matched_route_path_kwargs
                return matched_route(request)

            except Exception as e:
                exc_handler = self.exception_handlers.get(type(e))
                if exc_handler:
                    return exc_handler(request, e)
                raise e

        return dispatcher

    def add_exception_handler(self, exc_cls: Type[Exception], fn: Callable):
        self.exception_handlers[exc_cls] = fn

    def exception_handler(self, exc_cls: Type[Exception]) -> Callable:
        def _decorated(fn: Callable) -> Callable:
            self.add_exception_handler(exc_cls=exc_cls, fn=fn)

        return _decorated
