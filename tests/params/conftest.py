import pytest

from aiostipy import AppFactory, Controller, Get, Module
from aiostipy.params import Query, ReqBody
from aiostipy.responses import JSONResponse, Response


class TestAppController(Controller):
    prefix = "/"

    @Get("/body")
    async def get_body(self, body: ReqBody) -> Response:
        return JSONResponse(body)


class TestAppModule(Module):
    controllers = [TestAppController]


@pytest.fixture
async def client(aiohttp_client):
    app = AppFactory.create(TestAppModule)
    client = await aiohttp_client(app)
    return client
