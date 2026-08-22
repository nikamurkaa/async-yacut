import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        'sqlite:///db.sqlite3',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 30,
        },
    }
    DISK_TOKEN = os.getenv('DISK_TOKEN', '')
    MAX_CONTENT_LENGTH = int(
        os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024)
    )
