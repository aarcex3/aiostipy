import inspect
from typing import List

from aiohttp import web
from opyoid import AbstractModule

from aiostipy.core.container import AppContainer


class Application:

    @classmethod
    def create(
        cls, modules: List[AbstractModule | type[AbstractModule]], *args, **kwargs
    ) -> web.Application:
        cls._app: web.Application = web.Application(*args, **kwargs)
        container: AppContainer = AppContainer(modules)
        for module in modules:
            for controller in getattr(module, "controllers", []):
                controller_instance = container.get_module(controller)
                prefix = getattr(controller_instance, "prefix")

                for name, handler in inspect.getmembers(
                    controller_instance, predicate=inspect.ismethod
                ):
                    if not name.startswith("_"):
                        method: str = getattr(handler, "method")
                        path: str = getattr(handler, "path")
                        full_path = prefix if path == "/" else f"{prefix}{path}"
                        if method and path is not None:
                            cls._app.router.add_route(method, full_path, handler)
                return cls._app
