from inspect import isclass, isfunction

from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Union,
)
from string import Formatter
import re

from pydantic import BaseModel, Field

from django.utils.encoding import force_text

from .base import Request, Response

from .enums import AllowHttpMethodEnum


class RouteConfig(BaseModel):
    route_path: str = Field(..., min_length=1, regex=r"^/")
    allow_methods: List[AllowHttpMethodEnum] = Field(min_items=1)
    summary: Optional[str]
    description: Optional[str]
    tags: List[str]


class RoutePath(object):
    def __init__(self, route_path: str):
        route_path = force_text(route_path)
        assert route_path.startswith("/")

        self.org_route_path = route_path
        # route_path = route_path[1:]
        self.route_path = route_path[:-1] if route_path.endswith("/") else route_path

        self.key_set = set()
        re_segs = []
        fmt = Formatter()
        for prefix, key, fmt_spec, conversion in fmt.parse(self.route_path):
            if key is None:
                re_segs.append(prefix)
                continue

            assert key and not fmt_spec and not conversion, (
                "fail parsing parameter from path: " + self.route_path
            )
            assert key not in self.key_set, "duplicated key {}".format(key)
            self.key_set.add(key)
            re_segs.append("{prefix}(?P<{key}>[^/]+)".format(prefix=prefix, key=key))

        # print('regex: ' + ''.join(re_segs))
        self.regex = re.compile("^" + "".join(re_segs) + "$")

    def parse(self, request_path) -> Optional[Dict[str, str]]:
        if not request_path.startswith("/"):
            request_path = "/" + request_path

        match = self.regex.match(request_path)
        if not match:
            return None

        return match.groupdict()


def get_name(endpoint: Callable) -> str:
    if isfunction(endpoint) or isclass(endpoint):
        return endpoint.__name__

    return endpoint.__class__.__name__


class BaseRoute:
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        name: Optional[str] = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        include_in_schema: bool = True,
    ) -> None:
        self.path = path
        self.endpoint: Callable = endpoint
        self.name = name if name is not None else get_name(endpoint)
        self.path_parser: RoutePath = RoutePath(path)

        if methods is None:
            methods = ["GET"]
        self.methods: Set[str] = set([method.upper() for method in methods])

        self.include_in_schema: bool = include_in_schema

        def route_handler(request):
            return self.endpoint(request)

        self.route_handler: Callable[[Request], Response] = route_handler

    def match_path(self, request_path) -> Dict[str, str]:
        return self.path_parser.parse(request_path)

    def check_method_allowed(self, method):
        return method in self.methods

    def __call__(self, request: Request) -> Response:
        return self.route_handler(request)


class Router:
    def __init__(
        self,
        routes: Sequence[BaseRoute] = None,
        redirect_slashes: bool = True,
    ):
        self.routes = [] if routes is None else list(routes)
        self.redirect_slashes = redirect_slashes

    def add_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
    ) -> None:
        route = BaseRoute(
            path=path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)
