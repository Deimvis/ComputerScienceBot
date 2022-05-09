from functools import wraps


def apply(*nargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*nargs, *args, **kwargs)
        return wrapper
    return decorator
