"""Исключения, используемые сервисом YaCut."""

from http import HTTPStatus


class InvalidAPIUsage(Exception):
    """Ошибка запроса к API с сообщением и HTTP-статусом."""

    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        """Сохранить сообщение и HTTP-статус ошибки API."""
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ShortIDAlreadyExistsError(Exception):
    """Ошибка при попытке занять существующий короткий идентификатор."""

    pass


class YandexDiskError(Exception):
    """Ошибка при обращении к API Яндекс Диска."""

    pass
