# < ---------------------------------- > #

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.routes import app_routing

# < ---------------------------------- > #

app = Flask(__name__)

# < ---------------------------------- > #

app.register_blueprint(app_routing)

# < ---------------------------------- > #

app.config.from_object(Config)

# < ---------------------------------- > #

login_manager = LoginManager()
login_manager.init_app(app)

# < ---------------------------------- > #

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# < ---------------------------------- > #
