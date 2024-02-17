from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

class UploadForm(FlaskForm):
    data_name = StringField('Enter a name for this data set:', validators=[DataRequired()])
    csv_file = FileField('Choose a file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!'),
        FileSize(max_size=100 * 1024, message='File must be less than 100kb'),
    ])

    submit = SubmitField('Upload')

class StoreForm(FlaskForm):
    submit = SubmitField('Store this csv data')

app = Flask(__name__)
bootstrap = Bootstrap(app)

#this is for development purposes only,
app.config['SECRET_KEY'] = 'Its the end of the world as we know it and I feel fine'

#for non-dev, store a key en env and use:
#app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

app.debug = True

@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/data', methods=['GET', 'POST'])
def data():  # put application's code here
    csv_name = None
    upload_form = UploadForm()
    store_form = StoreForm()
    #data_table = None
    csv_html = None
    is_final_commit = False

    if upload_form.validate_on_submit():
        csv_name = upload_form.data_name.data
        csv_to_pd = pd.read_csv(upload_form.csv_file.data)
        csv_html = (csv_to_pd.to_html(index=False
                               , classes='table table-bordered table-striped'
                               , table_id='data_table'))
        #data_sql = csv_to_pd.to_sql('data_table')
        upload_form.data_name.data = ''

    elif store_form.validate_on_submit():
        is_final_commit = True

        #write to database

    return render_template('data.html'
                           , upload_form=upload_form
                           , store_form=store_form
                           , data_name=csv_name
                           , table=csv_html
                           , is_final_commit=is_final_commit)


@app.route('/viz')
def viz():  # put application's code here
    return render_template('viz.html', name='Tom')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
