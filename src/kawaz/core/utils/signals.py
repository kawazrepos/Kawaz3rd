from functools import wraps


def disable_for_loaddata(fn):
    """
    A decorator that turn off signal handlers when loading fexture data.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('raw', False):
            return
        fn(*args, **kwargs)
    return wrapper
