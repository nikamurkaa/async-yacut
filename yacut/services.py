"""Сервисные функции для работы с короткими ссылками."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from yacut import db
from yacut.constants import RESERVED_SHORT_IDS
from yacut.exceptions import ShortIDAlreadyExistsError
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


def short_id_exists(short_id):
    """Проверить наличие короткого идентификатора в базе данных."""
    return db.session.scalar(
        select(URLMap.id).where(URLMap.short == short_id)
    ) is not None


def create_url_map(original, custom_id=None):
    """Создать и сохранить связь исходного URL с коротким адресом."""
    if custom_id and (
        custom_id in RESERVED_SHORT_IDS or short_id_exists(custom_id)
    ):
        raise ShortIDAlreadyExistsError

    while True:
        short_id = custom_id or get_unique_short_id()
        url_map = URLMap(original=original, short=short_id)
        db.session.add(url_map)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if custom_id:
                raise ShortIDAlreadyExistsError
            continue
        return url_map


def get_url_map(short_id):
    """Получить запись по короткому идентификатору."""
    return db.session.scalar(
        select(URLMap).where(URLMap.short == short_id)
    )
