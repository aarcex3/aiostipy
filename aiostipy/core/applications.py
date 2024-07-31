from typing import Any, Type

from aiohttp import web

from aiostipy.core.container import AppContainer


class Application:
    _app: web.Application

    @classmethod
    def create(self, module: Type[Any]) -> web.Application:
        self._app: web.Application = web.Application()
        container: AppContainer = AppContainer()

        for provider in getattr(module, "_providers", []):
            container.register(provider)

        for controller in getattr(module, "_controllers", []):
            instance = container.resolve(controller)
            for routes in getattr(instance, "_routes", []):
                self._app.router.add_routes(routes)

    def run(self, *args, **kwargs):
        web.run_app(self._app, *args, **kwargs)
