import os
import tmdbsimple
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-secure-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'databases/shows.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    tmdbsimple.API_KEY = 'your-api-key-here'
