"""
Base route controller
"""

from aiohttp import web

from aiostipy.service import Service


class Controller(web.RouteTableDef):
    """
    Definition of base controller
    """

    def __init__(self, service: Service):
        super().__init__()
        self.service = service
