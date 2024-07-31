from typing import Any, Type


def Service(name: str):
    def wrapper(cls: Type[Any]):
        cls._service_name = name
        return cls

    return wrapper
