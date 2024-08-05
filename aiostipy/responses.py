from typing import Any, Callable, Optional

import msgspec
from aiohttp.typedefs import LooseHeaders
from aiohttp.web import Response
from multidict import CIMultiDict


class JSONResponse(Response):

    def __init__(
        self,
        data: Any = None,
        *,
        status: int = 200,
        reason: Optional[str] = None,
        headers: Optional[LooseHeaders] = None,
        content_type: str = "application/json",
        charset: Optional[str] = "utf-8",
        dumps: Callable = msgspec.json.encode,
    ) -> None:
        if headers is None:
            headers = CIMultiDict()

        body = dumps(data) if data is not None else None

        super().__init__(
            body=body,
            status=status,
            reason=reason,
            headers=headers,
            content_type=content_type,
            charset=charset,
        )
