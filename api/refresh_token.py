from functools import wraps


class AutoRefreshMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
        for name, value in clsobj.__dict__.items():
            if name.startswith('__'):
                continue
            if callable(value):
                setattr(clsobj, name, auto_refresh(value))
        return clsobj


def auto_refresh(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._lark_client.refresh_authorization()
        return func(self, *args, **kwargs)

    return wrapper
