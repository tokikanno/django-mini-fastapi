# from fastapi.security.base import SecurityBase
class SecurityBase:
    pass


# from fastapi.security.oauth2 import OAuth2, SecurityScopes
class OAuth2:
    pass


# from fastapi.security.oauth2 import OAuth2, SecurityScopes
class SecurityScopes:
    def __init__(self, *, scopes) -> None:
        self.scopes = scopes


# from fastapi.security.open_id_connect_url import OpenIdConnect
class OpenIdConnect:
    pass


# from starlette.concurrency import iterate_in_threadpool as iterate_in_threadpool  # noqa
async def iterate_in_threadpool(*args, **kwargs):
    pass


# from starlette.concurrency import run_in_threadpool as run_in_threadpool  # noqa
async def run_in_threadpool(*args, **kwargs):
    pass


# from starlette.concurrency import (  # noqa
#     run_until_first_complete as run_until_first_complete,
# )
async def run_until_first_complete(*args, **kwargs):
    pass


# from starlette.websockets import WebSocket
class WebSocket:
    pass


# from starlette.requests import HTTPConnection
class HTTPConnection:
    pass


# from starlette.background import BackgroundTasks
class BackgroundTasks:
    pass
