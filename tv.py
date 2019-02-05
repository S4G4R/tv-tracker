# < ---------------------------------- > #

# Import required packages
from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# < ---------------------------------- > #

# Flask app instance
app = Flask(__name__)

# < ---------------------------------- > #

# Load configurations
app.config.from_object(Config)

# < ---------------------------------- > #

# Set up database
db = SQLAlchemy(app)

from app import models

db.create_all()
# < ---------------------------------- > #

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

# < ---------------------------------- > #

# Import all the routes
from app.routes import app_routing
app.register_blueprint(app_routing)

# < ---------------------------------- > #
