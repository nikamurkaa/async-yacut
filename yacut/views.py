"""Маршруты пользовательского веб-интерфейса YaCut."""

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
)

from yacut import app
from yacut.constants import FILES_PREFIX
from yacut.disk import upload_files
from yacut.exceptions import ShortIDAlreadyExistsError, YandexDiskError
from yacut.forms import FileUploadForm, URLMapForm
from yacut.models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Показать форму и обработать создание короткой ссылки."""
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template(
            'index.html',
            form=form,
            short_link=None,
        )

    try:
        url_map = URLMap.create(
            form.original_link.data,
            form.custom_id.data,
        )
    except ShortIDAlreadyExistsError as error:
        flash(str(error), 'error')
        short_link = None
    else:
        short_link = url_map.to_dict()['short_link']
    return render_template(
        'index.html',
        form=form,
        short_link=short_link,
    )


@app.route(f'/{FILES_PREFIX}', methods=['GET', 'POST'])
async def files_view():
    """Показать форму и обработать загрузку файлов на Яндекс Диск."""
    form = FileUploadForm()
    if not form.validate_on_submit():
        return render_template(
            'files.html',
            form=form,
            uploaded_files=[],
        )

    uploaded_files = []
    try:
        disk_files = await upload_files(
            form.files.data,
            current_app.config['DISK_TOKEN'],
        )
        for filename, download_url in disk_files:
            url_map = URLMap.create(download_url)
            uploaded_files.append({
                'filename': filename,
                'short_link': url_map.to_dict()['short_link'],
            })
    except ShortIDAlreadyExistsError as error:
        flash(str(error), 'error')
    except YandexDiskError as error:
        flash(str(error), 'error')
    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Перенаправить по исходному URL короткой ссылки."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
