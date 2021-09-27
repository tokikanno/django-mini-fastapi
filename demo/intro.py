from datetime import datetime
from hashlib import md5
from typing import List, Optional

from django.http.response import Http404

try:
    from django import setup as django_setup
except ImportError:

    def django_setup():
        pass


from django.http import HttpResponseRedirect
from django.conf.urls import url
from pydantic import BaseModel, Field
from django_mini_fastapi import (
    OpenAPI,
    Path,
    Body,
    Query,
    Form,
    File,
    UploadFile,
    Cookie,
    Header,
    Request,
    Session,
    Response,
    Depends,
)


"""
A minimal working demo of Django App
"""

DEBUG = True
SECRET_KEY = "canukeepasecret"
ROOT_URLCONF = __name__

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


django_setup()


def redirect_to_doc(request):
    return HttpResponseRedirect(
        "/intro/rapidoc#tag--1.-Setup-your-first-OpenAPI-endpoint"
    )


api = OpenAPI(
    title="OpenAPI Test",
    version="0.1",
    description="Just a Test",
    root_path="/intro",
)

urlpatterns = [
    url(r"^$", redirect_to_doc),
    api.as_django_url_pattern(),
]


class IntroResponse1(BaseModel):
    arg1: str
    arg2: str


class IntroResponse2(BaseModel):
    arg1: str = Field(min_length=3, max_length=10)
    arg2: int = Field(ge=0, le=10)
    arg3: bool = Field(False)


@api.get(
    "/basic_get_request",
    tags=["1. Setup your first OpenAPI endpoint"],
    summary="Get start & create a simple http GET route",
)
def basic_get_request():
    """
    For start using django-mini-fastapi, in your Django project

    * import OpenAPI from django_mini_fastapi
    * create an OpenAPI object
    * put it into your urlpatterns
    * start define api endpoints using api OpenAPI object


    ```python
    from django_mini_fastapi import OpenAPI

    api = OpenAPI(
        title='OpenAPI Test',
        version='0.1',
        description='Just a Test',
        root_path='/intro'
    )

    urlpatterns = [
        api.as_django_url_pattern()
    ]

    @api.get('/basic_get_request')
    def basic_get_request():
        return {'hello': 'world'}
    ```
    """
    return {"hello": "world"}


@api.get(
    "/test_path_and_query_parameters/{arg1}",
    tags=["1. Basic HTTP requests"],
    summary="Define path & query parameters",
    response_model=IntroResponse1,
)
def test_path_and_query_parameters(
    arg1,
    arg2,
):
    """
    Use same arg name as the one in path for receiving path args
    For those args which names not matched path arg names, will be parsed as query parameter

    ```python
    from django_mini_fastapi import Path

    @api.get('/test_path_and_query_parameters/{arg1}')
    def test_path_and_query_parameters(arg1, arg2):
        return dict(arg1=arg1, arg2=arg2)
    ```
    """
    return dict(arg1=arg1, arg2=arg2)


@api.get(
    "/basic_check_on_path_or_query_parameter/{arg1}",
    tags=["1. Basic HTTP requests"],
    summary="Validate query string parameters",
    response_model=IntroResponse1,
)
def basic_check_on_path_or_query_parameter(
    arg1: int = Path(..., ge=0), arg2: str = Query("default", min_length=3)
):
    """
    Use `Query()` or `Path()` to tell API how to parse and check constraints of parameters

    ```python
    from django_mini_fastapi import Query, Path

    @api.get('/basic_check_on_path_or_query_parameter/{arg1}')
    def basic_check_on_path_or_query_parameter(arg1: int=Path(..., ge=0), arg2: str=Query('default')):
        return dict(arg1=arg1, arg2=arg2)
    ```
    """
    return dict(arg1=arg1, arg2=arg2)


@api.get(
    "/get_request_with_json_schema_query_args",
    tags=["1. Basic HTTP requests"],
    summary="Auto parameter validation via JSON schema fields",
    response_model=IntroResponse2,
)
def get_request_with_json_schema_query_args(
    arg1: str = Query(..., min_length=3, max_length=10),
    arg2: int = Query(..., ge=0, le=10),
    arg3: bool = Query(False),
):
    """
    ```python
    from django_mini_fastapi import Query

    @api.get('/get_request_with_json_schema_query_args')
    def get_request_with_json_schema_query_args(
        arg1: str = Query(..., min_length=3, max_length=10),
        arg2: int = Query(..., ge=0, le=10),
        arg3: bool = Query(False),
    ):
        return dict(arg1=arg1, arg2=arg2, arg3=arg3)
    ```
    """
    return dict(arg1=arg1, arg2=arg2, arg3=arg3)


@api.post(
    "/post_request_with_json_schema_form_args",
    tags=["1. Basic HTTP requests"],
    summary="Define Form parameters",
    response_model=IntroResponse2,
)
def post_request_with_json_schema_form_args(
    arg1: str = Form(..., min_length=3, max_length=10),
    arg2: int = Form(..., ge=0, le=10),
    arg3: bool = Form(False),
):
    """
    Now we use the same JSON schema field definitions, but in Form() format.

    ```python
    from django_mini_fastapi import Form
    from django_mini_fastapi.schema import StringField, NumberField, BooleanField

    @api.post('/post_request_with_json_schema_form_args')
    def post_request_with_json_schema_form_args(
        arg1: str = Form(..., min_length=3, max_length=10),
        arg2: int = Form(..., ge=0, le=10),
        arg3: bool = Form(False),
    ):
        return dict(arg1=arg1, arg2=arg2, arg3=arg3)
    ```
    """
    return dict(arg1=arg1, arg2=arg2, arg3=arg3)


@api.post(
    "/post_request_file_upload",
    tags=["1. Basic HTTP requests"],
    summary="Define File Upload",
)
def post_request_file_upload(
    upload_file: UploadFile = File(...),
    md5_hash: Optional[str] = Form(None, description="md5 of uploaded file"),
):
    """
    Now let's try building an endpoint for user file upload.

    ```python
    from hashlib import md5
    from django_mini_fastapi import UploadedFile, Form, File

    @api.post('/post_request_file_upload')
    def post_request_file_upload(
        upload_file: UploadedFile = File(...),
        md5_hash: Optional[str] = Form(None, description="md5 of uploaded file"),
    ):
        return {
            'submitted_md5': md5_hash,
            'file': {
                'name': upload_file.name,
                'size': upload_file.size,
                'md5': md5(upload_file.read()).hexdigest,
            },
        }
    ```
    """
    return {
        "submitted_md5": md5_hash,
        "file": {
            "name": upload_file.name,
            "size": upload_file.size,
            "md5": md5(upload_file.read()).hexdigest(),
        },
    }


class SamplePayload(BaseModel):
    arg1: str = Field(..., min_length=3, max_length=10)
    arg2: int = Field(..., ge=0, le=10)
    arg3: bool = Field(..., default_value=False)


class SampleResponse(BaseModel):
    obj: SamplePayload
    ary: List[SamplePayload]


@api.post(
    "/post_request_with_json_schema_body",
    tags=["1. Basic HTTP requests"],
    summary="Define body parameters via JSON schema model",
    response_model=SampleResponse,
)
def post_request_with_json_schema_body(payload: SamplePayload):
    """
    The JSON schema fields could also be used for describing JSON body format,
    all you need is declearing a class inherited from BaseModel class.

    ```python
    from pydantic import BaseModel, Field

    class SamplePayload(BaseModel):
        arg1: str = Field(..., min_length=3, max_length=10)
        arg2: int = Field(..., ge=0, le=10)
        arg3: bool = Field(..., default_value=False)


    class SampleResponse(BaseModel):
        obj: SamplePayload
        ary: List[SamplePayload]


    @api.post(
        '/post_request_with_json_schema_body',
        response_model=SampleResponse,  # you can also put json schema model here for declearing response model
    )
    def post_request_with_json_schema_body(
        payload: SamplePayload,
    ):
        return payload
    ```
    """
    return {"obj": payload, "ary": [payload, payload]}


@api.post(
    "/accessing_special_raw_variables",
    tags=["1. Basic HTTP requests"],
    summary="Some special variables",
)
def accessing_special_raw_variables(
    request: Request, session: Session, response: Response
):
    """
    You could access some special variables via your function parameter type.

    * `django_mini_fast_api.Request`

      * For accessing the raw django `HttpRequest` object

    * `django_mini_fast_api.Session`

      * django session object binded on request

    * ``django_mini_fast_api.Response``

      * A temp empty response for manipulating/overriding status code / headers / cookies on the final response object

    ```python
    @api.get(
        '/accessing_special_raw_variables',
    )
    def accessing_special_raw_variables(request: Request, session: Session, response: Response):

        current_dt_str = str(datetime.now())
        response.set_cookie("test_cookie", current_dt_str)
        response["X-TEST-HEADER"] = current_dt_str

        session["ts"] = current_dt_str
        session.save()

        return {
            'request': request,
            'session': session,
        }
    ```
    """
    current_dt_str = str(datetime.now())
    response.set_cookie("test_cookie", current_dt_str)
    response["X-TEST-HEADER"] = current_dt_str

    session["ts"] = current_dt_str
    session.save()

    return {
        "request": repr(request),
        "session": session,
    }


@api.post(
    "/other_argument_data_sources",
    tags=["1. Basic HTTP requests"],
    summary="Other argument data sources",
)
def other_argument_data_sources(
    test_cookie=Cookie(...), referer=Header(...), x_api_token=Header(...)
):
    """
    You can also get your request arguments from other data sources.

    Like: `Header()`, `Cookie()`

    * *Note: While accessing via `Header()`, all variable name will converted to uppercase as http header key name*
    * *e.g.: `content_type` -> `CONTENT_TYPE`

    ```python
    @api.post(
        '/other_argument_data_sources',
    )
    def other_argument_data_sources(
        test_cookie=Cookie(...), referer=Header(...), x_api_token=Header(...)
    ):
        return {
            "test_cookie": test_cookie,
            "x_api_token": x_api_token,
            "referer": referer,
        }
    ```
    """
    return {
        "test_cookie": test_cookie,
        "x_api_token": x_api_token,
        "referer": referer,
    }


class Pagination(BaseModel):
    page: int
    limit: int


def get_pagination(page: int = Query(1, ge=1), limit: int = Query(20, ge=0)):
    return Pagination(page=page, limit=limit)


@api.get(
    "/basic_dependencies",
    tags=["2. Dependencies"],
    summary="Basic dependencies sample",
)
def basic_dependencies(pagination: Pagination = Depends(get_pagination)):
    """
    For common operations across multiple API endpoints, you could use Depends() for merging them into single dependency functions

    For example:
    You need to parse pagination info on each API endpoint, you could write a `get_pagination` function and let your API endpoint `Depends()` on it.

    ```python
    class Pagination(BaseModel):
        page: int
        limit: int

    def get_pagination(page: int = Query(1, ge=1), limit: int = Query(20, ge=0)):
        return Pagination(page=page, limit=limit)

    @api.get("/basic_dependencies")
    def basic_dependencies(
        pagination: Pagination = Depends(get_pagination)
    ):
        return {"pagination": pagination}
    ```
    """
    return {"pagination": pagination}


def check_api_key(x_api_key: str = Header(...)):
    if x_api_key != "kamehame":
        raise Http404


@api.get(
    "/non_return_dependencies",
    tags=["2. Dependencies"],
    summary="Dependencies without return value",
    dependencies=[Depends(check_api_key)],
)
def non_return_dependencies():
    """
    For dependencies only need to be executed but needn't to return any values, you could declear it in API endpoint declaration function with `dependencies=` keyword argument

    For example:
    You need to check API key on every API endpoint, you could write a `check_api_key` function put into API endpoint's (even router) dependencies

    ```python
    def check_api_key(x_api_key: str = Header(...)):
        if x_api_key != "kamehame":
            raise Http404

    @api.get("/non_return_dependencies", dependencies=[Depends(check_api_key)],)
    def non_return_dependencies():
        return {"msg": "You have correct API key!"}
    ```
    """
    return {"msg": "You have correct API key!"}
