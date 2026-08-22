"""Тесты структуры моделей базы данных."""

from sqlalchemy import inspect

from yacut.models import URLMap


def test_fields(_app):
    """Проверить обязательные поля модели URLMap."""
    inspector = inspect(URLMap)
    fields = [column.name for column in inspector.columns]
    assert all(field in fields for field in
               ['id', 'original', 'short', 'timestamp']), (
        'В модели `URLMap` не найдены все необходимые поля. '
        'Проверьте модель: в ней должны быть поля `id`, `original`, `short` '
        'и `timestamp`.'
    )
