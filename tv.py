# < ---------------------------------- > #

from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# < ---------------------------------- > #

app = Flask(__name__)

# < ---------------------------------- > #

app.config.from_object(Config)

# < ---------------------------------- > #

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

db.create_all()

# TODO Set up database migration
# < ---------------------------------- > #

from app.routes import app_routing
app.register_blueprint(app_routing)

# < ---------------------------------- > #

login_manager = LoginManager()
login_manager.init_app(app)

# < ---------------------------------- > #
