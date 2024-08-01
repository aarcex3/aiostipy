from typing import Any, Type

from aiohttp import web

from aiostipy.core.container import AppContainer


class Application:

    @classmethod
    def create(cls, module: Type[Any], *args, **kwargs) -> web.Application:
        cls._app: web.Application = web.Application(*args, **kwargs)
        container: AppContainer = AppContainer()

        for provider in getattr(module, "_controllers", []):
            container.register(provider)

        for controller in getattr(module, "_controllers", []):
            instance = container.resolve(controller)
            for route in getattr(instance, "_routes", []):
                cls._app.router.add_route(
                    path=route.path,
                    method=route.method,
                    handler=route.handler,
                )
        return cls._app
