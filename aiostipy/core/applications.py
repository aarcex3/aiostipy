from typing import Any, Type

from aiohttp import web

from aiostipy.core.container import AppContainer


class Application:

    @classmethod
    def create(self, module: Type[Any], *args, **kwargs) -> web.Application:
        self._app: web.Application = web.Application(*args, **kwargs)
        container: AppContainer = AppContainer()

        for provider in getattr(module, "_providers", []):
            container.register(provider)

        for controller in getattr(module, "_controllers", []):
            instance = container.resolve(controller)
            for routes in getattr(instance, "_routes", []):
                self._app.router.add_routes(routes)
        return self._app
