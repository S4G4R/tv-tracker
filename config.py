import os
import tmdbsimple
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)

class Config(object):
    SQLALCHEMY_DATABASE_URI         = 'sqlite:////' + os.path.join(basedir, 'databases/shows.db')
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SECRET_KEY                      = os.environ.get("SECRET_KEY")
    tmdbsimple.API_KEY              = os.environ.get("API_KEY")
