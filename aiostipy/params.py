from typing import Any

from aiohttp import web
from aiohttp_extracts import Cookie as Cookie
from aiohttp_extracts import MatchInfo as Param
from aiohttp_extracts import Parameter
from aiohttp_extracts import QueryAttr as Query
from multidict import MultiMapping


class File(Parameter):
    def __init__(
        self, name: str, filename: str, content: bytes, headers: MultiMapping[str]
    ):
        self.name = name
        self.filename = filename
        self.content = content
        self.headers = headers

    @classmethod
    async def extract(cls, request: web.Request, name: str) -> "File":
        if cls.name:
            name = cls.name
        reader = await request.multipart()

        async for part in reader:
            if part.name == name:
                filename = part.filename
                content = await part.read(decode=True)
                headers = part.headers

                return cls(
                    name=name, filename=filename, content=content, headers=headers
                )

        return None


class Header(Parameter):

    @classmethod
    async def extract(cls, name: str, request: web.Request) -> str:
        if cls.name:
            name = cls.name
        name = (
            name.capitalize()
            if len(name) == 1
            else "-".join(word.capitalize() for word in name.split("_"))
        )
        return request.headers.get(name)


class Query(Parameter):

    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Any:
        name = cls.name or name
        value = request.query.get(name)

        if value is None:
            raise web.HTTPBadRequest(reason=f"Missing query parameter '{name}'.")
        if cls.type:
            try:
                return cls.type(value)
            except (ValueError, TypeError):
                raise web.HTTPBadRequest(
                    reason=f"Invalid type for query parameter '{name}'. Expected {cls.type.__name__}."
                )

        return value
