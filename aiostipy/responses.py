import json
from typing import Any, Optional

from aiohttp.typedefs import LooseHeaders
from multidict import CIMultiDict

from aiostipy.datastructures import Response


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
        dumps: Optional[callable] = json.dumps,
    ) -> None:
        if headers is None:
            headers = CIMultiDict()

        if data is not None:
            body = dumps(data).encode(charset)
        else:
            body = None

        super().__init__(
            body=body,
            status=status,
            reason=reason,
            headers=headers,
            content_type=content_type,
            charset=charset,
        )
