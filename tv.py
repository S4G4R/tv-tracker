# < ---------------------------------- > #

from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# < ---------------------------------- > #

app = Flask(__name__)

# < ---------------------------------- > #

app.config.from_object(Config)

# < ---------------------------------- > #

db = SQLAlchemy(app)

from app import models

db.create_all()
# < ---------------------------------- > #

login_manager = LoginManager()
login_manager.init_app(app)

# < ---------------------------------- > #

from app.routes import app_routing
app.register_blueprint(app_routing)

# < ---------------------------------- > #
