import re
from http import HTTPStatus

from flask import jsonify, request, url_for

from yacut import app
from yacut.constants import (
    CUSTOM_ID_MAX_LENGTH,
    CUSTOM_ID_PATTERN,
    DUPLICATED_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
    RESERVED_SHORT_IDS,
)
from yacut.exceptions import InvalidAPIUsage, ShortIDAlreadyExistsError
from yacut.services import create_url_map, get_url_map


def validate_custom_id(custom_id):
    if custom_id in (None, ''):
        return None
    if (
        not isinstance(custom_id, str)
        or len(custom_id) > CUSTOM_ID_MAX_LENGTH
        or re.fullmatch(CUSTOM_ID_PATTERN, custom_id) is None
    ):
        raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
    if custom_id in RESERVED_SHORT_IDS:
        raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)
    return custom_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not isinstance(data, dict) or 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = validate_custom_id(data.get('custom_id'))
    try:
        url_map = create_url_map(data['url'], custom_id)
    except ShortIDAlreadyExistsError:
        raise InvalidAPIUsage(DUPLICATED_SHORT_ID_MESSAGE)
    return jsonify({
        'url': url_map.original,
        'short_link': url_for(
            'redirect_view',
            short_id=url_map.short,
            _external=True,
        ),
    }), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', strict_slashes=False)
def get_original_link(short_id):
    url_map = get_url_map(short_id)
    if url_map is None:
        raise InvalidAPIUsage(
            'Указанный id не найден',
            HTTPStatus.NOT_FOUND,
        )
    return jsonify({'url': url_map.original})
