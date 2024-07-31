from typing import Any, Sequence, Type


def Module(
    controllers: Sequence[Type[Any]] = [],
    providers: Sequence[Type[Any]] = [],
    imports: Sequence[Type[Any]] = [],
    exports: Sequence[Type[Any]] = [],
):
    """
    Definition of module decorator
    """

    def wrapper(cls: Type[Any]) -> Type[Any]:
        cls._controllers = controllers
        cls._providers = providers
        cls._imports = imports
        cls._exports = exports
        return cls

    return wrapper
