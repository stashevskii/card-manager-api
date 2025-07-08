from functools import wraps
from typing import Callable, Any
from app.api.errors import BUSINESS2HTTP


def handle_business_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            try:
                raise BUSINESS2HTTP[e.__class__]
            except KeyError:
                return

    return wrapper
