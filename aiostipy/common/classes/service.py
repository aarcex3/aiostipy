from abc import ABC

from opyoid import SingletonScope
from opyoid.scopes import Scope


class Service(ABC):

    scope: type[Scope] = SingletonScope
