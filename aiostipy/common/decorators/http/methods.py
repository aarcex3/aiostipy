"""
Definition of http methods decorators
"""

from typing import Optional


def Get(path: Optional[str] = "/"):

    def wrapper(func):
        func.method = "GET"
        func.path = path
        return func

    return wrapper


def Post(path: Optional[str] = "/"):

    def wrapper(func):
        func.method = "POST"
        func.path = path
        return func

    return wrapper


def Put(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "PUT"
        func.path = path
        return func

    return wrapper


def Delete(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "DELETE"
        func.path = path
        return func

    return wrapper


def Head(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "HEAD"
        func.path = path
        return func

    return wrapper


def Options(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "OPTIONS"
        func.path = path
        return func

    return wrapper


def Patch(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "PATCH"
        func.path = path
        return func

    return wrapper


def Static(path: Optional[str] = "/"):
    def wrapper(func):
        func.method = "STATIC"
        func.path = path
        return func

    return wrapper


def View(
    path: str,
):
    def wrapper(func):
        func.method = "VIEW"
        func.path = path
        return func

    return wrapper
