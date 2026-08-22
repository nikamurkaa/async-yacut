from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)

from yacut import app
from yacut.constants import DUPLICATED_SHORT_ID_MESSAGE
from yacut.disk import upload_files
from yacut.exceptions import ShortIDAlreadyExistsError, YandexDiskError
from yacut.forms import FileUploadForm, URLMapForm
from yacut.services import create_url_map, get_url_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    short_link = None
    if form.validate_on_submit():
        try:
            url_map = create_url_map(
                form.original_link.data,
                form.custom_id.data or None,
            )
        except ShortIDAlreadyExistsError:
            flash(DUPLICATED_SHORT_ID_MESSAGE, 'error')
        else:
            short_link = url_for(
                'redirect_view',
                short_id=url_map.short,
                _external=True,
            )
    return render_template(
        'index.html',
        form=form,
        short_link=short_link,
    )


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileUploadForm()
    uploaded_files = []
    if form.validate_on_submit():
        try:
            disk_files = await upload_files(
                form.files.data,
                current_app.config['DISK_TOKEN'],
            )
            for filename, download_url in disk_files:
                url_map = create_url_map(download_url)
                uploaded_files.append({
                    'filename': filename,
                    'short_link': url_for(
                        'redirect_view',
                        short_id=url_map.short,
                        _external=True,
                    ),
                })
        except YandexDiskError as error:
            flash(str(error), 'error')
    return render_template(
        'files.html',
        form=form,
        uploaded_files=uploaded_files,
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    url_map = get_url_map(short_id)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
