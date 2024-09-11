import pytest

from aiostipy import AppFactory, Controller, Get, Module, Request
from aiostipy.common.decorators.http.methods import Post
from aiostipy.params import Cookie, File, Header, Path, Query, ReqBody
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

    @Get("/request")
    async def get_request(self, request: Request) -> Response:
        message = await request.json()
        return JSONResponse(message)

    @Get("/get_path/{a}/{b}")
    async def get_path(self, a: Path[int], b: Path[int]) -> Response:
        return JSONResponse({"result": a + b})

    @Post("/post_file")
    async def post_file(self, file: File) -> Response:
        return JSONResponse(
            {"filename": file.filename, "content": file.content.decode()}
        )


class TestAppModule(Module):
    controllers = [TestAppController]


@pytest.fixture
async def client(aiohttp_client):
    app = AppFactory.create(TestAppModule)
    client = await aiohttp_client(app)
    return client
