"""Minimal FastAPI implementation for Django"""

__version__ = "0.1.8"


from .api import OpenAPI as OpenAPI
from .base import (
    Request as Request,
    Response as Response,
    UploadFile as UploadFile,
    Session as Session,
)
from .fastapi.param_functions import (
    Path as Path,
    Query as Query,
    Form as Form,
    File as File,
    Body as Body,
    Header as Header,
    Cookie as Cookie,
    Depends as Depends,
)
from .fastapi.routing import APIRoute as APIRoute
from .fastapi.routing import APIRouter as APIRouter

from .fastapi.exceptions import HTTPException as HTTPException
