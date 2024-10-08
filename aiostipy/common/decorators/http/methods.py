from __future__ import annotations

import inspect
import json
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union

import msgspec
from aiohttp import hdrs, web
from aiohttp.web import Request as Request
from aiohttp.web import Response as Response

from aiostipy.params import Parameter
from aiostipy.responses import JSONResponse

FunctionParams = Dict[
    str, Tuple[Union[Type[web.Request], Type[Parameter], Type[type]], Optional[Any]]
]
AsyncFunc = Callable[..., Awaitable[web.Response]]


def fetch_fn_params(fn: Callable) -> FunctionParams:
    fn_params = {}
    params = inspect.signature(fn).parameters
    for param_name, param in params.items():
        if param_name == "self":
            continue
        annotation = param.annotation
        default = param.default
        if default is param.empty:
            default = None
        if annotation is param.empty:
            raise ValueError(
                "Parameter {} of function {} has no type hint".format(param_name, fn)
            )
        fn_params[param.name] = (annotation, default)
    return fn_params


async def handle_request(
    func: Callable, request: web.Request, kwargs: Dict[str, Any]
) -> Callable:

    async def deserialize_body(model_class):
        body: str = await request.text()
        if not body.strip():
            raise web.HTTPBadRequest(
                reason="Request body is empty, but data was expected"
            )
        try:
            deserialized_data = msgspec.json.decode(body, type=model_class)
        except json.JSONDecodeError as ex:
            raise web.HTTPBadRequest(
                reason="Invalid JSON format in request body"
            ) from ex

        return deserialized_data

    async def wrapper(self, *args, **kwargs):
        func_params: FunctionParams = fetch_fn_params(func)

        for name, (type, default) in func_params.items():
            if isinstance(type, Type) and issubclass(type, web.Request):
                kwargs[name] = request
            if isinstance(type, Type) and issubclass(type, msgspec.Struct):
                kwargs[name] = await deserialize_body(type)
            if isinstance(type, Type) and issubclass(type, Parameter):
                kwargs[name] = await type.extract(name=name, request=request) or default
            else:
                kwargs[name] = kwargs.get(name, default)
        return await func(self, *args, **kwargs)

    return wrapper


def handle_response(
    response: Union[Dict, str, web.Response, bytes, Any]
) -> web.Response:
    if isinstance(response, dict):
        return JSONResponse(data=response)
    elif isinstance(response, str):
        return web.Response(text=response, content_type="text/plain")
    elif isinstance(response, web.Response):
        return response
    else:
        return JSONResponse(data=response)


def route_decorator(method: str) -> AsyncFunc:
    def decorator(
        path: Optional[str] = "/",
        description: Optional[str] = None,
        summary: Optional[str] = None,
        responses: Dict[int, str] = None,
        deprecated: bool = False,
    ) -> Callable:
        def wrapper(func: Callable) -> Callable:
            @wraps(func)
            async def wrapped(
                self, request: web.Request, *args, **kwargs
            ) -> web.Response:

                try:
                    func_with_params = await handle_request(func, request, kwargs)
                    response = await func_with_params(self, *args, **kwargs)
                    return handle_response(response=response)
                except Exception as ex:
                    raise web.HTTPBadRequest(
                        reason=f"Invalid request data. Error -> {ex}"
                    ) from ex

            wrapped.method = method
            wrapped.path = path
            wrapped.description = description
            wrapped.summary = summary
            wrapped.responses = responses
            wrapped.deprecated = deprecated
            return wrapped

        return wrapper

    return decorator


Get = route_decorator(hdrs.METH_GET)
Post = route_decorator(hdrs.METH_POST)
Put = route_decorator(hdrs.METH_PUT)
Delete = route_decorator(hdrs.METH_DELETE)
Head = route_decorator(hdrs.METH_HEAD)
Options = route_decorator(hdrs.METH_OPTIONS)
Trace = route_decorator(hdrs.METH_TRACE)
