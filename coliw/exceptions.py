def get_code(exc):
    if not exc:
        return 0
    if isinstance(exc, BaseError):
        return exc.CODE
    return BaseError.CODE


class BaseError(Exception):

    CODE = 1


class ParseError(BaseError):

    CODE = 10


class CallError(BaseError):

    CODE = 20
