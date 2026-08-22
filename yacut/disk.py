import asyncio
from uuid import uuid4

import aiohttp

from yacut.constants import YANDEX_DISK_API_URL, YANDEX_DISK_DIRECTORY
from yacut.exceptions import YandexDiskError


def normalize_filename(filename):
    normalized = filename.replace('\\', '/').rsplit('/', 1)[-1]
    return normalized.replace('\x00', '') or 'file'


async def upload_file(session, filename, content):
    disk_filename = normalize_filename(filename)
    disk_path = f'{YANDEX_DISK_DIRECTORY}/{uuid4().hex}_{disk_filename}'

    async with session.get(
        f'{YANDEX_DISK_API_URL}/upload',
        params={
            'path': disk_path,
            'overwrite': 'true',
            'fields': 'href',
        },
    ) as response:
        response.raise_for_status()
        upload_url = (await response.json()).get('href')
    if not upload_url:
        raise YandexDiskError('Яндекс Диск не вернул ссылку для загрузки.')

    async with session.put(upload_url, data=content) as response:
        response.raise_for_status()

    async with session.get(
        f'{YANDEX_DISK_API_URL}/download',
        params={'path': disk_path, 'fields': 'href'},
    ) as response:
        response.raise_for_status()
        download_url = (await response.json()).get('href')
    if not download_url:
        raise YandexDiskError('Яндекс Диск не вернул ссылку для скачивания.')
    return filename, download_url


async def upload_files(files, token):
    if not token:
        raise YandexDiskError('Не настроен токен доступа к Яндекс Диску.')

    payloads = [(file.filename, file.read()) for file in files]
    timeout = aiohttp.ClientTimeout(total=120)
    headers = {'Authorization': f'OAuth {token}'}
    try:
        async with aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
        ) as session:
            return await asyncio.gather(*(
                upload_file(session, filename, content)
                for filename, content in payloads
            ))
    except (aiohttp.ClientError, TimeoutError) as error:
        raise YandexDiskError(
            'Не удалось загрузить файлы на Яндекс Диск.'
        ) from error
