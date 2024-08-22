import inspect
from typing import List

from aiohttp import web
from aiohttp_swagger import setup_swagger
from opyoid import AbstractModule

from aiostipy.common.classes.controller import Controller
from aiostipy.common.classes.module import Module
from aiostipy.core.container import AppContainer


class Application:

    @classmethod
    def create(
        cls,
        modules: List[Module | AbstractModule | type[AbstractModule]],
        *args,
        **kwargs,
    ) -> web.Application:
        cls._app: web.Application = web.Application(*args, **kwargs)
        container: AppContainer = AppContainer(modules)
        for module in modules:
            for controller in module.controllers:
                controller_instance: Controller = container.get_module(controller)
                prefix = controller_instance.prefix

                for name, handler in inspect.getmembers(
                    controller_instance, predicate=inspect.ismethod
                ):
                    if not name.startswith("_"):
                        method: str = handler.method
                        path: str = handler.path

                        if path == "/":
                            full_path = prefix
                        else:

                            full_path = f"{prefix.rstrip('/')}/{path.lstrip('/')}"

                        if method and path is not None:
                            cls._app.router.add_route(
                                method=method,
                                path=full_path,
                                handler=handler,
                                name=f"{controller.__name__.lower()}_{name.lower()}",
                            )
        setup_swagger(cls._app, ui_version=3)
        return cls._app
