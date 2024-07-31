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
    routes: list[RouteDef] = []

    def decorator(cls: Type):
        cls._route_prefix = path
        for _, obj in inspect.getmembers(cls):
            if isinstance(obj, RouteDef):
                obj.path = (
                    cls._route_prefix + obj.path
                    if cls._route_prefix != "/"
                    else obj.path
                )
                routes.append(obj)
        cls._routes = routes
        return cls

    return decorator
