"""Дополнительные тесты публичного контракта YaCut."""

import re
from http import HTTPStatus

from tests.conftest import PY_URL


def test_files_short_id_is_reserved_in_api(client):
    """Проверить запрет идентификатора files через API."""
    response = client.post('/api/id/', json={
        'url': PY_URL,
        'custom_id': 'files',
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json == {
        'message': 'Предложенный вариант короткой ссылки уже существует.'
    }


def test_get_api_accepts_url_without_trailing_slash(
    client,
    short_python_url,
):
    """Проверить API-запрос без завершающей косой черты."""
    response = client.get(f'/api/id/{short_python_url.short}')

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'url': short_python_url.original}


def test_generated_short_link_is_ascii_alphanumeric(client):
    """Проверить формат автоматически созданного идентификатора."""
    response = client.post('/api/id/', json={'url': PY_URL})
    short_id = response.json['short_link'].rsplit('/', 1)[-1]

    assert re.fullmatch(r'[A-Za-z0-9]{6}', short_id)


def test_proxy_headers_are_used_for_external_url(client):
    """Проверить построение внешнего URL с учётом прокси-заголовков."""
    response = client.post(
        '/api/id/',
        json={'url': PY_URL},
        headers={
            'Host': 'kirta-security.ru',
            'X-Forwarded-Proto': 'https',
        },
    )

    assert response.json['short_link'].startswith(
        'https://kirta-security.ru/'
    )
