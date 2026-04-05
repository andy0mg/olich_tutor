"""HTTP middleware (корреляция запросов, access-лог)."""

from backend.middleware.access_log import AccessLogMiddleware

__all__ = ["AccessLogMiddleware"]
