import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'So long and thanks for all the fish'