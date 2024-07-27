"""
App definition
"""

from typing import Optional, Type, TypeVar

from typing_extensions import Annotated, Doc

from aiostipy.datastructures import Application
from aiostipy.responses import JSONResponse, Response

AppType = TypeVar("AppType", bound="Aiostipy")


class Aiostipy(Application):
    """Aiostipy class definition"""

    def __init__(
        self: AppType,
        title: Annotated[
            str,
            Doc(
                """
                The title of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Example**

                ```python
                from aiostipy import Aiostipy

                app = Aiostipy(title="ChimichangApp")
                ```
                """
            ),
        ] = "",
        summary: Annotated[
            Optional[str],
            Doc(
                """
                A short summary of the API.

                It will be added to the generated OpenAPI (e.g. visible at `/docs`).

                **Example**

                ```python
                from aiostipy import Aiostipy

                app = Aiostipy(summary="ChimichangApp")
                ```
                """
            ),
        ] = "",
        version: Annotated[str, Doc()] = "",
        default_response_class: Annotated[
            Type[Response],
            Doc(
                """
                The default response class to be used.

                **Example**

                ```python
                from aiostipy import Aiostipy
                from aiostipy.responses import JSONResponse

                app = Aiostipy(default_response_class=JSONResponse)
                ```
                """
            ),
        ] = JSONResponse,
    ):
        super().__init__()
