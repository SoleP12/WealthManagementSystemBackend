from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from backend.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not settings.testing
    )