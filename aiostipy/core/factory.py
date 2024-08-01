from typing import Any, Type

from aiohttp import web

from aiostipy.core.applications import Application


class AppFactory:

    @classmethod
    def create(cls, module: Type[Any]):
        cls._app = Application.create(module)
        return cls._app
