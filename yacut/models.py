"""Модели базы данных сервиса YaCut."""

from datetime import datetime, timezone
from random import choices

from flask import url_for
from sqlalchemy.exc import IntegrityError

from yacut import db
from yacut.constants import (
    CUSTOM_ID_MAX_LENGTH,
    RESERVED_SHORT_IDS,
    SHORT_ID_ALPHABET,
    SHORT_ID_LENGTH,
)
from yacut.exceptions import ShortIDAlreadyExistsError


class URLMap(db.Model):
    """Связь исходного URL с коротким идентификатором."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(CUSTOM_ID_MAX_LENGTH),
        unique=True,
        nullable=False,
        index=True,
    )
    timestamp = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    @staticmethod
    def get_unique_short_id():
        """Сгенерировать свободный короткий идентификатор."""
        while True:
            short_id = ''.join(choices(
                SHORT_ID_ALPHABET,
                k=SHORT_ID_LENGTH,
            ))
            if (
                short_id not in RESERVED_SHORT_IDS
                and URLMap.query.filter_by(short=short_id).first() is None
            ):
                return short_id

    @staticmethod
    def create(original, custom_id=None):
        """Создать и сохранить новую короткую ссылку."""
        if custom_id and (
            custom_id in RESERVED_SHORT_IDS
            or URLMap.query.filter_by(short=custom_id).first() is not None
        ):
            raise ShortIDAlreadyExistsError

        url_map = URLMap(
            original=original,
            short=custom_id or URLMap.get_unique_short_id(),
        )
        db.session.add(url_map)
        try:
            db.session.commit()
        except IntegrityError as error:
            db.session.rollback()
            raise ShortIDAlreadyExistsError from error
        return url_map

    @staticmethod
    def get(short_id):
        """Получить запись по короткому идентификатору."""
        return URLMap.query.filter_by(short=short_id).first()

    def to_dict(self):
        """Представить короткую ссылку в формате ответа API."""
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_view',
                short_id=self.short,
                _external=True,
            ),
        }
