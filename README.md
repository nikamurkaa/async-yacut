# YaCut

Сервис сокращения ссылок на **Flask** с REST API и асинхронной загрузкой файлов на Яндекс Диск.

Проект объединяет классический URL shortener, веб-интерфейс и API. Пользователь может задать собственный короткий идентификатор или получить автоматически сгенерированный. Для файлов реализована отдельная страница `/files`: несколько файлов загружаются на Яндекс Диск асинхронно, после чего сервис создаёт короткую ссылку для каждого результата.

## Возможности

- создание коротких ссылок через веб-интерфейс;
- создание и получение ссылок через REST API;
- автоматическая генерация уникальных short ID;
- проверка пользовательских идентификаторов и защита от конфликтов;
- редирект с короткой ссылки на исходный URL;
- асинхронная загрузка нескольких файлов через `aiohttp`;
- интеграция с API Яндекс Диска;
- отдельная обработка ошибок веб-интерфейса и API;
- миграции базы данных через Flask-Migrate/Alembic;
- контейнеризация приложения с Nginx и Docker Compose;
- pytest-тесты и проверка стиля через flake8.

## Стек технологий

| Компонент | Технологии |
| --- | --- |
| Backend | Python, Flask, Gunicorn |
| Database | SQLite, SQLAlchemy |
| Migrations | Flask-Migrate, Alembic |
| Async I/O | aiohttp, asyncio |
| Frontend | Jinja2, Bootstrap |
| API | REST, OpenAPI |
| Infrastructure | Docker, Docker Compose, Nginx |
| Testing | pytest, pytest-asyncio, flake8 |

## Архитектура

Основная логика разделена по ответственности:

```text
yacut/
├── api_views.py       # REST API
├── views.py           # веб-маршруты
├── models.py          # SQLAlchemy-модель и работа с short ID
├── forms.py           # WTForms
├── disk.py            # асинхронная интеграция с Яндекс Диском
├── error_handlers.py  # обработчики ошибок
├── exceptions.py      # пользовательские исключения
├── constants.py       # константы приложения
└── templates/         # Jinja2-шаблоны
```

Конфликты коротких идентификаторов обрабатываются на уровне модели через `ShortIDAlreadyExistsError`. Сообщение передаётся вместе с исключением, а слой представления использует его при формировании ответа пользователю или API.

## API

| Метод | Endpoint | Назначение |
| --- | --- | --- |
| `POST` | `/api/id/` | Создать короткую ссылку |
| `GET` | `/api/id/<short_id>/` | Получить исходный URL |

Полная схема запросов, ответов и ошибок находится в [`openapi.yml`](openapi.yml). Для ручной проверки также доступна коллекция в [`postman_collection/`](postman_collection/).

## Локальный запуск

Клонируйте репозиторий:

```bash
git clone https://github.com/nikamurkaa/async-yacut.git
cd async-yacut
```

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте `.env` на основе примера:

```bash
cp .env.example .env
```

Пример конфигурации:

```dotenv
FLASK_APP=yacut
SECRET_KEY=replace-with-a-random-secret
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=replace-with-a-yandex-disk-token
MAX_CONTENT_LENGTH=104857600
```

Для работы загрузки файлов потребуется OAuth-токен Яндекс Диска с необходимыми правами доступа.

Примените миграции и запустите приложение:

```bash
flask db upgrade
flask run
```

После запуска сервис будет доступен на `http://127.0.0.1:5000`.

## Запуск в Docker

Создайте конфигурацию окружения:

```bash
cp .env.example infra/.env
```

Для SQLite внутри контейнера укажите:

```dotenv
DATABASE_URI=sqlite:////app/data/yacut.db
```

Запустите сервисы:

```bash
docker compose -f infra/compose.yml up -d --build
```

Nginx будет доступен на `http://localhost` и проксировать запросы в Gunicorn-приложение.

## Тесты и качество кода

```bash
pytest
flake8 .
```

Тесты покрывают работу модели, API, редиректы, обработку ошибок и асинхронную загрузку файлов.

## Автор

[Николь Журбенко](https://github.com/nikamurkaa)

Проект выполнен в рамках курса **«Python-разработчик» Яндекс Практикума**.
