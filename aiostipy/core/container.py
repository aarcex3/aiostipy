from typing import Any, Type


class AppContainer:
    """
    Container class definition
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppContainer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._providers = {}

    def register(self, provider: Type[Any]):
        self._providers[provider.__hash__] = provider

    def resolve(self, provider: Type[Any]) -> Any:
        return self._providers[provider.__hash__]()
