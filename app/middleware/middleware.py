from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.database import async_session_maker


class DBSessionMiddleware(BaseHTTPMiddleware):
    """Добавление сессии БД в запрос (request.state.db) и передача его дальше в цепочку обработки"""
    async def dispatch(self, request: Request, call_next) -> Response:
        async with async_session_maker() as session:
            request.state.db = session
            response = await call_next(request)
        return response
