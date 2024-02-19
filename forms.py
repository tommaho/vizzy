from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    data_name = StringField('Enter a name for this data set:', validators=[DataRequired()])
    csv_file = FileField('Choose a file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!'),
        FileSize(max_size=100 * 1024, message='File must be less than 100kb'),
    ])

    upload = SubmitField('Upload')


class StoreForm(FlaskForm):
    store = SubmitField('Store Data')
    abort = SubmitField('Abort')