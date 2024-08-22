from typing import Any, List, Optional, Type

from opyoid import AbstractModule, InjectedT, Injector

from aiostipy.common.classes.module import Module


class AppContainer(Injector):

    def __init__(
        self, modules: Optional[List[Module | AbstractModule | type[AbstractModule]]]
    ):
        super().__init__(modules)

    def get_module(self, client: Type[Any]) -> InjectedT:
        return self.inject(client)
