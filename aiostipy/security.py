from __future__ import annotations

from typing import Optional

from aiohttp import BasicAuth, hdrs, web
from aiohttp_extracts import Parameter


class HTTPBasicAuth(Parameter):
    @classmethod
    async def extract(cls, name: str, request: web.Request) -> BasicAuth:
        auth_header: Optional[str] = request.headers.get(hdrs.AUTHORIZATION)
        if not auth_header:
            return None

        try:
            auth = BasicAuth.decode(auth_header)
        except (ValueError, IndexError):
            return None

        return auth
