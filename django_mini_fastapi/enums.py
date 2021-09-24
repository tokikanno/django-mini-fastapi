from enum import Enum


class StrEnum(str, Enum):
    pass


class AllowHttpMethodEnum(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    TRACE = "TRACE"
    OPTION = "OPTION"
