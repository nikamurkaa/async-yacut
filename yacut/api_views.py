"""Эндпоинты API для создания и получения коротких ссылок."""

import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.constants import (
    CUSTOM_ID_MAX_LENGTH,
    CUSTOM_ID_PATTERN,
    INVALID_SHORT_ID_MESSAGE,
)
from yacut.exceptions import InvalidAPIUsage, ShortIDAlreadyExistsError
from yacut.models import URLMap


def validate_custom_id(custom_id):
    """Проверить пользовательский короткий идентификатор."""
    if custom_id and (
        not isinstance(custom_id, str)
        or len(custom_id) > CUSTOM_ID_MAX_LENGTH
        or re.fullmatch(CUSTOM_ID_PATTERN, custom_id) is None
    ):
        raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создать короткую ссылку из данных POST-запроса."""
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not isinstance(data, dict) or 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get('custom_id')
    validate_custom_id(custom_id)
    try:
        url_map = URLMap.create(data['url'], custom_id)
    except ShortIDAlreadyExistsError as error:
        raise InvalidAPIUsage(str(error)) from error
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', strict_slashes=False)
def get_original_link(short_id):
    """Вернуть исходный URL по короткому идентификатору."""
    url_map = URLMap.get_by_short_id(short_id)
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND,
        )
    return jsonify({'url': url_map.to_dict()['url']})
