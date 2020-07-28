from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

# config app instance from config.py class
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# create mail server, pulling app.config from config.py and env variables
mail = Mail(app)

# create SQLAlchemy db instance from app with configs above
db = SQLAlchemy(app)

# init Bcrypt
bcrypt = Bcrypt(app)

# init LoginManager
login_manager = LoginManager(app)
# TODO: confirm this section of login manager uses the right app. routing
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# init Marshmallow
ma = Marshmallow(app)
