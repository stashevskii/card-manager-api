from fastapi import Request, Response
from time import perf_counter
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        now = perf_counter()
        response = await call_next(request)
        response.headers["X-Process-Time"] = f"{perf_counter() - now:.2f} ms"
        return response
