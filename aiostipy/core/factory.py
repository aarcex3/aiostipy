import asyncio

import uvloop

from aiostipy.core.applications import Application


class AppFactory:

    @classmethod
    def create(cls, module):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        cls._app = Application.create([module])
        return cls._app
