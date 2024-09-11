from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterable, Mapping, Optional, Type, TypeVar, Union

from aiohttp import BodyPartReader, MultipartReader, web
from aiohttp.web_exceptions import HTTPException
from multidict import CIMultiDictProxy

from .meta import ParameterMeta

T = TypeVar("T")


class Parameter(ABC, Generic[T], metaclass=ParameterMeta):
    name: Optional[Type[str]]
    type: Optional[Type[T]]

    def __init__(
        self, name: Optional[str] = None, type: Optional[Type[T]] = None
    ) -> None:
        self.name: str = name
        self.type: Type[T] = type

    @classmethod
    @abstractmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional[T]:
        """
        Abstract class method to extract data from a request.
        This method should be implemented by subclasses.
        """

    @staticmethod
    def __parse_key__(key: Union[str, type, Iterable]) -> Dict[str, Any]:
        """
        Parses the key to determine the name and type attributes.
        This is a static method as it doesn't rely on instance or class-level data.
        """
        params: Dict[str, Any] = {}

        if isinstance(key, str):
            params["name"] = key
        if isinstance(key, type):
            params["type"] = key
        if isinstance(key, Iterable):
            params.update({k: v for k, v in zip(("name", "type"), key)})
        return params

    def __repr__(self) -> str:
        return "{}(name: {}, type: {})".format(
            self.__class__.__name__, self.name, self.type
        )


class Header(Parameter[str]):
    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> str:
        name = (
            name.capitalize()
            if len(name) == 1
            else "-".join(word.capitalize() for word in name.split("_"))
        )
        value = request.headers.get(name)
        if value is None:
            raise web.HTTPBadRequest(reason=f"Missing header '{name}'.")
        return value


class Cookie(Parameter[str]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional[str]:
        cookie = request.cookies.get(name)
        if cookie:
            return cookie
        else:
            raise web.HTTPBadRequest(reason=f"Missing cookie '{name}'")


class ReqBody(Parameter[Dict[str, Any]]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Dict[str, Any]:
        if request.can_read_body:
            return await request.json()
        else:
            raise web.HTTPBadRequest(reason="Request body is missing.")


class Path(Parameter[T]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional[T]:
        value = request.match_info.get(name)
        if cls.type:
            try:
                return cls.type(value)
            except (ValueError, TypeError):
                raise web.HTTPBadRequest(
                    reason=f"Invalid type for path parameter '{name}'. Expected {cls.type.__name__}."
                )


class Query(Parameter[T]):
    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> T:
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


class RequestAttr(Parameter[str]):
    name: Optional[str] = None

    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> Any:
        return request.get(name, None)


class File(Parameter[bytes]):
    def __init__(
        self,
        name: str,
        filename: Optional[str],
        content: bytes,
        headers: Union[Mapping[str, str], CIMultiDictProxy[str]],
    ):
        super().__init__(name=name, type=bytes)
        self.filename = filename
        self.content = content
        self.headers = headers

    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional["File"]:
        try:
            reader: MultipartReader = await request.multipart()

            async for part in reader:
                if isinstance(part, BodyPartReader):
                    if getattr(part, "name", None) == name:
                        filename = getattr(part, "filename", None)
                        content = await part.read(decode=True)
                        headers = getattr(part, "headers", {})

                        return cls(
                            name=name,
                            filename=filename,
                            content=content,
                            headers=headers,
                        )
        except Exception as e:
            raise HTTPException(text=f"{e}") from e
