from typing import Any, Type

from aiohttp import web

from aiostipy.core.applications import Application


class AppFactory:
    _app: Application

    @classmethod
    def create(self, module: Type[Any]):
        self._app = Application.create(module)
        return self._app
