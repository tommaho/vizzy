from flask import Flask, render_template
from flask_bootstrap import Bootstrap

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


@app.route('/data')
def data():  # put application's code here
    return render_template('data.html', name='Tom')


@app.route('/viz')
def viz():  # put application's code here
    return render_template('viz.html', name='Tom')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
