from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from cloud.config import Config 

# app instance
app = Flask(__name__)
# configuration file vars
app.config.from_object(Config)
# db instance
db = SQLAlchemy(app)
# migrations
migrate = Migrate(app, db)
# Manage logins
login = LoginManager(app)
login.login_view = 'users.login'

from cloud import main, models

# Blueprints
from cloud.users.users import users

app.register_blueprint(users, url_prefix='/user')



