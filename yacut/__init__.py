"""Инициализация Flask-приложения, базы данных и расширений YaCut."""

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .settings import Config


app = Flask(
    __name__,
    static_folder='../html',
    static_url_path='/static',
)
app.config.from_object(Config)
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,
    x_proto=1,
    x_host=1,
)

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

from .models import URLMap  # noqa: E402


@app.shell_context_processor
def make_shell_context():
    """Добавить объекты базы данных в контекст Flask Shell."""
    return {'db': db, 'URLMap': URLMap}


from . import api_views, error_handlers, views  # noqa: E402, F401
