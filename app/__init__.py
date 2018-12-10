# < ---------------------------------- > #

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)

from app import routes

# < ---------------------------------- > #

login_manager = LoginManager()
login_manager.init_app(app)

# < ---------------------------------- > #

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# < ---------------------------------- > #
