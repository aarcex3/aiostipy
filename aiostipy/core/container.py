from typing import Any, List, Optional, Type

from opyoid import AbstractModule, Injector


class AppContainer(Injector):

    def __init__(self, modules: Optional[List[AbstractModule | type[AbstractModule]]]):
        super().__init__(modules)

    def get_module(self, client: Type[Any]) -> Any:
        return self.inject(client)
