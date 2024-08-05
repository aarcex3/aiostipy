from typing import Any, List, Type

import opyoid


class Module(opyoid.Module):
    controllers: List[Type[Any]] = []
    services: List[Type[Any]] = []
    imports: List[Type[Any]] = []
    exports: List[Type[Any]] = []  

    def configure(self) -> None:
        if self.controllers:
            for controller in self.controllers:
                self.bind(controller)
        if self.services:
            for service in self.services:
                self.bind(service)
        if self.imports:
            for module in self.imports:
                self.install(module)
