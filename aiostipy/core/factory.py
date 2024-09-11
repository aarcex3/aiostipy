import uvloop

from aiostipy.core.applications import Application


class AppFactory:

    @classmethod
    def create(cls, module):

        cls._app = Application.create([module])
        return cls._app
