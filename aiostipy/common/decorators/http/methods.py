"""
Definition of http methods decorators
"""

from typing import Optional

from aiohttp import web
from aiohttp.web_routedef import RouteDef


def Get(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.get(path=path, handler=func, **kwargs)

    return wrapper


def Post(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.post(path=path, handler=func, **kwargs)

    return wrapper


def Put(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.put(path=path, handler=func, **kwargs)

    return wrapper


def Delete(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.delete(path=path, handler=func, **kwargs)

    return wrapper


def Head(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.head(path=path, handler=func, **kwargs)

    return wrapper


def Options(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.options(path=path, handler=func, **kwargs)

    return wrapper


def Patch(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.patch(path=path, handler=func, **kwargs)

    return wrapper


def Static(path: Optional[str] = "/", **kwargs):
    def wrapper(func) -> RouteDef:
        return web.static(path=path, handler=func, **kwargs)

    return wrapper


def View(path: str, **kwargs):
    def wrapper(func) -> RouteDef:
        return web.view(path=path, handler=func, **kwargs)

    return wrapper
