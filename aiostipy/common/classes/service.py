from opyoid import SingletonScope
from opyoid.scopes import Scope


class Service:
    scope: type[Scope] = SingletonScope
