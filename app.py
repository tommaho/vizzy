from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pandas as pd

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    csv_file = FileField('Choose a file', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!'),
        FileSize(max_size=100 * 1024, message='File must be less than 100kb'),
    ])

    submit = SubmitField('Submit')

app = Flask(__name__)
bootstrap = Bootstrap(app)

#this is for development purposes only,
app.config['SECRET_KEY'] = 'Its the end of the world as we know it and I feel fine'

#for non-dev, store a key en env and use:
#app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

app.debug = True

@app.route('/')
def home():  # put application's code here
    return render_template('index.html', name='Tom')


@app.route('/data', methods=['GET', 'POST'])
def data():  # put application's code here
    name = None
    form = NameForm()
    data_table = None
    if form.validate_on_submit():
        name = form.name.data
        data_table = (pd.read_csv(form.csv_file.data)
                      .to_html(index=False
                               , classes='table table-bordered table-striped'
                               , table_id='data_table'))
        form.name.data = ''
    return render_template('data.html'
                           , form=form
                           , name=name
                           , table=data_table)


@app.route('/viz')
def viz():  # put application's code here
    return render_template('viz.html', name='Tom')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
