"""Константы для коротких ссылок и работы с Яндекс Диском."""

from string import ascii_letters, digits


SHORT_ID_ALPHABET = ascii_letters + digits
SHORT_ID_LENGTH = 6
CUSTOM_ID_MAX_LENGTH = 16
CUSTOM_ID_PATTERN = r'^[A-Za-z0-9]+$'
RESERVED_SHORT_IDS = frozenset({'files'})

DUPLICATED_SHORT_ID_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID_MESSAGE = (
    'Указано недопустимое имя для короткой ссылки'
)

YANDEX_DISK_API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
YANDEX_DISK_DIRECTORY = 'app:'
