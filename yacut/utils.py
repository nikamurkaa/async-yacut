"""Вспомогательные функции для генерации коротких ссылок."""

from random import choices

from sqlalchemy import select

from yacut import db
from yacut.constants import SHORT_ID_ALPHABET, SHORT_ID_LENGTH
from yacut.models import URLMap


def get_unique_short_id(length=SHORT_ID_LENGTH, reserved=None):
    """Сгенерировать свободный короткий идентификатор заданной длины."""
    reserved = reserved or set()
    while True:
        short_id = ''.join(choices(SHORT_ID_ALPHABET, k=length))
        exists = db.session.scalar(
            select(URLMap.id).where(URLMap.short == short_id)
        )
        if not exists and short_id not in reserved:
            return short_id
