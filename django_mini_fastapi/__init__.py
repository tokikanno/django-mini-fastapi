"""Minimal FastAPI implementation for Django"""

__version__ = "0.1"


from .api import OpenAPI as OpenAPI
from .base import (
    Request as Request,
    Response as Response,
    UploadFile as UploadFile,
    Session as Session,
)
from .fastapi.param_functions import Path, Query, Form, File, Body, Header, Cookie
from .fastapi.routing import APIRoute as APIRoute
from .fastapi.routing import APIRouter as APIRouter
