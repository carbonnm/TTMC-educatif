from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(Config)

login_manager = LoginManager(app)
#Redirect to login page
#login_manager.login_view = "login"

#Database part :
db = SQLAlchemy(app)

from application import routes