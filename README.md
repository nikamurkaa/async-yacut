# YaCut

## Описание проекта

YaCut — сервис для создания коротких ссылок. Пользователь может указать
собственный короткий идентификатор или получить автоматически сгенерированный.
При переходе по короткой ссылке сервис перенаправляет на исходный адрес.

На странице `/files` можно одновременно загрузить несколько файлов на
Яндекс Диск. Файлы загружаются асинхронно, после чего YaCut создаёт отдельную
короткую ссылку для скачивания каждого файла.

Основные возможности:

- создание коротких ссылок через веб-интерфейс и API;
- автоматическая генерация уникальных идентификаторов;
- переадресация на исходные адреса;
- асинхронная загрузка нескольких файлов на Яндекс Диск;
- отдельные обработчики ошибок для сайта и API.

Проект доступен по адресу: [kirta-security.ru](https://kirta-security.ru).

## Стек технологий

| Компонент | Технологии |
|---|---|
| Backend | Python 3.12, Flask, Gunicorn |
| База данных | SQLite, SQLAlchemy, Alembic |
| Асинхронные запросы | aiohttp |
| Интерфейс | Jinja2, Bootstrap |
| Инфраструктура | Docker Compose, Nginx, Let's Encrypt |

## Локальный запуск

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone https://github.com/kindarufy/async-yacut.git
cd async-yacut
```

Создайте и активируйте виртуальное окружение, установите зависимости:

```bash
python3.12 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Создайте файл с переменными окружения:

```bash
cp .env.example .env
```

Укажите необходимые значения в `.env`:

```dotenv
FLASK_APP=yacut
SECRET_KEY=replace-with-a-random-secret
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=replace-with-a-yandex-disk-token
MAX_CONTENT_LENGTH=104857600
```

Для `DISK_TOKEN` нужен OAuth-токен Яндекс Диска с правом
`cloud_api:disk.app_folder`.

Примените миграции и запустите сервер:

```bash
flask db upgrade
flask run
```

Сервис будет доступен по адресу `http://127.0.0.1:5000`.

## API

- `POST /api/id/` — создать короткую ссылку;
- `GET /api/id/<short_id>/` — получить исходный URL по короткому идентификатору.

Формат запросов, ответов и ошибок описан в файле
[`openapi.yml`](openapi.yml). Коллекция для проверки API находится в директории
[`postman_collection`](postman_collection).

## Проверка проекта

```bash
pytest
flake8 .
```

## Запуск в Docker

Создайте файл конфигурации для Docker Compose:

```bash
cp .env.example infra/.env
```

Для хранения SQLite в Docker укажите в `infra/.env`:

```dotenv
DATABASE_URI=sqlite:////app/data/yacut.db
```

Соберите и запустите контейнеры:

```bash
docker compose -f infra/compose.yml up -d --build
```

Конфигурация Nginx рассчитана на домен `kirta-security.ru` и сертификаты
Let's Encrypt в `/etc/letsencrypt`.

## Автор

[kindarufy](https://github.com/kindarufy)
