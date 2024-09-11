import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from aiostipy import AppFactory, Get, Module, Post


class TestAppService:
    name: str = "Testapp"
    version: str = "1.0.0"

    def get_app_info(self) -> dict[str, str]:
        return {"version": self.version, "name": self.name}

    def get_request_data(self, request: web.Request) -> dict[str, str]:
        return {"scheme": request.scheme}


class TestAppController:
    prefix = "/"

    def __init__(self, service: TestAppService):
        self.service = service

    @Get("/app_info")
    async def app_info(self, request: web.Request) -> web.Response:
        response = self.service.get_app_info()
        return web.json_response(response)

    @Post("/request_info")
    async def request_info(self, request: web.Request) -> web.Response:
        response = self.service.get_request_data(request)
        return web.json_response(response)


class TestAppModule(Module):
    controllers = [TestAppController]
    services = [TestAppService]


@pytest.fixture
async def client(aiohttp_client):
    app = AppFactory.create(TestAppModule)
    client = await aiohttp_client(app)
    return client
