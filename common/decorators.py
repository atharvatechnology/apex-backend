from functools import wraps


def disable_for_loaddata(signal_handler):
    """Decorate that turns off signal handlers when loading fixture data."""

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs.get("raw", False):
            return
        signal_handler(*args, **kwargs)

    return wrapper
