from flask import Flask, render_template, flash, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
import pandas as pd
import sqlite3

# DEPRECATED
import bleach


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.debug = True

if app.debug:
    app.config['SECRET_KEY'] = 'Its the end of the world as we know it and I feel fine'
else:
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')


basedir = os.path.abspath(os.path.dirname(__file__))
sqlite_db = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

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


def store_data(df, table_name):
    conn = sqlite3.connect(sqlite_db)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/manage')
def manage():
    flash('There are currently no datasets to manage. Upload and store a dataset.', 'warning')
    return render_template('manage.html')


@app.route('/data', methods=['GET', 'POST'])
def data():  # put application's code here
    flash('Free users can upload csv files only, max file size 100kb.', 'warning')
    csv_name = None
    upload_form = UploadForm()
    store_form = StoreForm()
    csv_df = None
    csv_html = None
    is_final_commit = False

    if store_form.validate_on_submit() and 'store' in request.form:
        data_json = session.get('data')
        if data_json:
            store_data(pd.read_json(data_json), 'test')

        is_final_commit = True
        flash('CSV stored, and available to Visualize or Manage.', 'success')

    elif store_form.validate_on_submit() and 'abort' in request.form:
        flash('File processing aborted.', 'danger')
    else:

        if upload_form.validate_on_submit():
            csv_name = upload_form.data_name.data

            csv_df = pd.read_csv(upload_form.csv_file.data, encoding='utf-8')

            # should break this out into a more robust custom converter on read_csv
            csv_df.map(lambda x: bleach.clean(x) if isinstance(x, str) else x)

            # stage this in a database for larger datasets, and where the preview steps
            # might include schema changes
            session['data'] = csv_df.to_json()

            csv_html = (csv_df.to_html(index=False
                                       , classes='table table-bordered table-striped'
                                       , table_id='data_table'))
            # data_sql = csv_to_pd.to_sql('data_table')
            upload_form.data_name.data = ''
            flash('CSV successfully uploaded.', 'success')

        elif upload_form.errors:
            flash('Invalid upload! csv files under 100kb only!', 'danger')

    return render_template('data.html'
                           , upload_form=upload_form
                           , store_form=store_form
                           , data_name=csv_name
                           , data_frame=csv_df
                           , table=csv_html
                           , is_final_commit=is_final_commit)


@app.route('/viz')
def viz():  # put application's code here
    flash('There are currently no datasets to visualize. Upload and store a dataset.', 'warning')
    return render_template('viz.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('na.html'), 404


if __name__ == '__main__':
    app.run()
