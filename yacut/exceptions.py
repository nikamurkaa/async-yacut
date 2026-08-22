from http import HTTPStatus


class InvalidAPIUsage(Exception):
    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ShortIDAlreadyExistsError(Exception):
    pass


class YandexDiskError(Exception):
    pass
