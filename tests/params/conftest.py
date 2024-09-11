import pytest

from aiostipy import AppFactory, Controller, Get, Module
from aiostipy.params import Query, ReqBody
from aiostipy.responses import JSONResponse, Response


class TestAppController(Controller):
    prefix = "/"

    @Get("/body")
    async def get_body(self, body: ReqBody) -> Response:
        return JSONResponse(body)

    @Get("/get_query")
    async def get_query(self, a: Query[int], b: Query[int]) -> Response:
        return JSONResponse({"result": a + b})

    @Get("/query_wrong_type")
    async def get_query_wrong_type(self, a: Query[int], b: Query[int]) -> Response:
        return JSONResponse({"result": a + b})


class TestAppModule(Module):
    controllers = [TestAppController]


@pytest.fixture
async def client(aiohttp_client):
    app = AppFactory.create(TestAppModule)
    client = await aiohttp_client(app)
    return client
