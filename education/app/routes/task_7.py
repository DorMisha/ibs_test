import logging
import time
import app.routes.logger as logger
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

#output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)


"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |
[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Load request ID from headers if present. Generate one otherwise."""
        global response
        start_time = time.time()
        try:
        # client_host.set(request.client.host)
        # output_log.info(f"Accepted request {request.method} {request.url}")
            response = await call_next(request)
        except Exception as e:
            logger.output_log.error(f"Error processing request: {e}")
            response = Response("Internal Server Error", status_code=500)
        finally:
            execution_time = time.time() - start_time
            logger.output_log.info(f"{execution_time:.2f} | {request.method} | {request.url} | {response.status_code}")

        return response
