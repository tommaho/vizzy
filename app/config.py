import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'So long and thanks for all the fish'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'data.sqlite'