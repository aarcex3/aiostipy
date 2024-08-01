"""
Base route controller
"""

import inspect
from typing import Optional, Type

from aiohttp.web_routedef import RouteDef


def Controller(path: Optional[str] = "/"):
    """
    Definition of controller decorator
    """

    def decorator(cls: Type):
        cls._route_prefix = path
        cls._routes = []
        for _, obj in inspect.getmembers(cls):
            if isinstance(obj, RouteDef):
                route_path = (
                    cls._route_prefix + obj.path
                    if cls._route_prefix != "/"
                    else obj.path
                )
                route = RouteDef(
                    path=route_path,
                    method=obj.method,
                    handler=obj.handler,
                    kwargs=obj.kwargs,
                )
                cls._routes.append(route)
        return cls

    return decorator
