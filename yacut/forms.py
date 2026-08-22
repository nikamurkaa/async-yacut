from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    URL,
    ValidationError,
)

from yacut.constants import CUSTOM_ID_MAX_LENGTH, CUSTOM_ID_PATTERN


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[DataRequired(), URL()],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Length(max=CUSTOM_ID_MAX_LENGTH),
            Regexp(CUSTOM_ID_PATTERN),
        ],
    )
    submit = SubmitField('Создать')


def files_required(form, field):
    if not field.data or not all(file.filename for file in field.data):
        raise ValidationError('Выберите хотя бы один файл.')


class FileUploadForm(FlaskForm):
    files = MultipleFileField('Файлы', validators=[files_required])
    submit = SubmitField('Загрузить')
