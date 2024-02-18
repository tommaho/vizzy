from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os
import pandas as pd
import bleach #DEPRECATED!

class UploadForm(FlaskForm):
    data_name = StringField('Enter a name for this data set:', validators=[DataRequired()])
    csv_file = FileField('Choose a file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!'),
        FileSize(max_size=100 * 1024, message='File must be less than 100kb'),
    ])

    submit = SubmitField('Upload')

class StoreForm(FlaskForm):
    submit = SubmitField('Store Data')
    cancel = SubmitField('Abort')

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.debug = True

if app.debug:
    app.config['SECRET_KEY'] = 'Its the end of the world as we know it and I feel fine'
else:
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def home():  # put application's code here
    return render_template('index.html')

@app.route('/manage')
def manage():  # put application's code here
    flash('There are currently no datasets to manage. Upload and store a dataset.', 'warning')
    return render_template('manage.html')

@app.route('/data', methods=['GET', 'POST'])
def data():  # put application's code here
    flash('Free users can upload csv files only, max file size 100kb.', 'warning')
    csv_name = None
    upload_form = UploadForm()
    store_form = StoreForm()
    csv_html = None
    is_final_commit = False

    if upload_form.validate_on_submit():
        csv_name = upload_form.data_name.data
        csv_df = pd.read_csv(upload_form.csv_file.data, encoding='utf-8')

        #should break this out into a more robust custom converter on read_csv
        csv_df.applymap(lambda x: bleach.clean(x) if isinstance(x, str) else x)

        csv_html = (csv_df.to_html(index=False
                               , classes='table table-bordered table-striped'
                               , table_id='data_table'))
        #data_sql = csv_to_pd.to_sql('data_table')
        upload_form.data_name.data = ''
        flash('CSV successfully uploaded.', 'success')
    #handle errror here!
    else:
        if upload_form.errors:
            flash('Invalid upload! csv files under 100kb only!', 'danger')

    # elif store_form.validate_on_submit():
    #     is_final_commit = True
    #
    #     #write to database
    #     flash('CSV stored, and available to Visualize or Manage.', 'success')

    return render_template('data.html'
                           , upload_form=upload_form
                           , store_form=store_form
                           , data_name=csv_name
                           , table=csv_html
                           , is_final_commit=is_final_commit)


@app.route('/viz')
def viz():  # put application's code here
    flash('There are currently no datasets to vizualize. Upload and store a dataset.', 'warning')
    return render_template('viz.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
