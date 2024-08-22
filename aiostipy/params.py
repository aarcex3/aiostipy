from aiohttp import web
from aiohttp_extracts import Cookie as Cookie
from aiohttp_extracts import Header as Header
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
