from __future__ import annotations

from typing import Any, List, Type

import opyoid

from .controller import Controller
from .service import Service


class Module(opyoid.Module):
    controllers: List[Type[Controller]] = []
    services: List[Type[Service]] = []
    imports: List[Type[Module]] = []
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
                for controller in module.controllers:
                    self.controllers.append(controller)
                for service in module.services:
                    self.services.append(service)
