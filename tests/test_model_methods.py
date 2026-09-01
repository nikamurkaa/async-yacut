"""Тесты методов модели для работы с короткими ссылками."""

import pytest
from sqlalchemy.exc import IntegrityError

from tests.conftest import PY_URL, TEST_BASE_URL
from yacut import db
from yacut.constants import (
    DUPLICATED_SHORT_ID_MESSAGE,
    FILES_PREFIX,
    RESERVED_SHORT_IDS,
)
from yacut.exceptions import ShortIDAlreadyExistsError
from yacut.models import URLMap


def test_create_get_and_to_dict(_app):
    """Проверить создание, поиск и представление записи в словаре."""
    url_map = URLMap.create(PY_URL, 'python')

    assert URLMap.get_by_short_id('python') == url_map
    with _app.test_request_context('/', base_url=TEST_BASE_URL):
        assert url_map.to_dict() == {
            'url': PY_URL,
            'short_link': f'{TEST_BASE_URL}/python',
        }


def test_reserved_short_id_is_rejected(_app):
    """Проверить отклонение зарезервированного идентификатора."""
    assert isinstance(RESERVED_SHORT_IDS, tuple)
    assert FILES_PREFIX in RESERVED_SHORT_IDS
    assert not URLMap.is_short_id_available(FILES_PREFIX)

    with pytest.raises(ShortIDAlreadyExistsError) as error_info:
        URLMap.create(PY_URL, FILES_PREFIX)

    assert str(error_info.value) == DUPLICATED_SHORT_ID_MESSAGE


def test_unique_short_id_skips_existing_value(_app, monkeypatch):
    """Проверить повторную генерацию при совпадении с записью в базе."""
    URLMap.create(PY_URL, 'AAAAAA')
    generated_values = iter(('AAAAAA', 'BBBBBB'))

    def generate_value(alphabet, k):
        """Вернуть очередное тестовое значение идентификатора."""
        return next(generated_values)

    monkeypatch.setattr('yacut.models.choices', generate_value)

    assert not URLMap.is_short_id_available('AAAAAA')
    assert URLMap.is_short_id_available('BBBBBB')
    assert URLMap.get_unique_short_id() == 'BBBBBB'


def test_create_commits_once(_app, monkeypatch):
    """Проверить единственный commit при создании записи."""
    original_commit = db.session.commit
    commit_calls = 0

    def tracked_commit():
        """Посчитать вызов и выполнить настоящий commit."""
        nonlocal commit_calls
        commit_calls += 1
        original_commit()

    monkeypatch.setattr(db.session, 'commit', tracked_commit)

    URLMap.create(PY_URL, 'single')

    assert commit_calls == 1


def test_create_rolls_back_after_integrity_error(_app, monkeypatch):
    """Проверить rollback и исключение при ошибке сохранения."""
    original_rollback = db.session.rollback
    rollback_calls = 0

    def failed_commit():
        """Имитировать ошибку ограничения базы данных."""
        raise IntegrityError(None, None, Exception())

    def tracked_rollback():
        """Посчитать вызов и выполнить настоящий rollback."""
        nonlocal rollback_calls
        rollback_calls += 1
        original_rollback()

    monkeypatch.setattr(db.session, 'commit', failed_commit)
    monkeypatch.setattr(db.session, 'rollback', tracked_rollback)

    with pytest.raises(ShortIDAlreadyExistsError) as error_info:
        URLMap.create(PY_URL, 'conflict')

    assert str(error_info.value) == DUPLICATED_SHORT_ID_MESSAGE
    assert rollback_calls == 1
