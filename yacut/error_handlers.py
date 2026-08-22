"""Обработчики ошибок пользовательского интерфейса и API."""

from http import HTTPStatus

from flask import jsonify, render_template

from yacut import app, db
from yacut.exceptions import InvalidAPIUsage


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Вернуть ошибку API в формате JSON."""
    return jsonify({'message': error.message}), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Показать страницу ошибки при отсутствии ресурса."""
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Откатить транзакцию и показать страницу серверной ошибки."""
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR
