import pytest

from aiostipy import AppFactory, Controller, Get, Module
from aiostipy.params import Cookie, Header, Query, ReqBody
from aiostipy.responses import JSONResponse, Response


class TestAppController(Controller):
    prefix = "/"

    @Get("/body")
    async def get_body(self, body: ReqBody) -> Response:
        return JSONResponse(body)

    @Get("/get_query")
    async def get_query(self, a: Query[int], b: Query[int]) -> Response:
        return JSONResponse({"result": a + b})

    @Get("/get_header")
    async def get_header(self, x_custom: Header["X-Custom"]) -> Response:
        return JSONResponse({"x_custom": x_custom})

    @Get("/get_cookie")
    async def get_cookie(self, my_cookie: Cookie) -> Response:
        return JSONResponse({"cookie": my_cookie})


class TestAppModule(Module):
    controllers = [TestAppController]


@pytest.fixture
async def client(aiohttp_client):
    app = AppFactory.create(TestAppModule)
    client = await aiohttp_client(app)
    return client
