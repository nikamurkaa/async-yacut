"""Модели базы данных сервиса YaCut."""

from datetime import datetime, timezone

from yacut import db


class URLMap(db.Model):
    """Связь исходного URL с коротким идентификатором."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(16),
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
