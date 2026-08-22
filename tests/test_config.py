"""Тесты конфигурации приложения YaCut."""


def test_config(default_app):
    """Проверить наличие секретного ключа Flask."""
    assert default_app.config.get('SECRET_KEY'), (
        'Проверьте, что задали значение для конфигурационного ключа '
        '`SECRET_KEY`.'
    )
