from config import Config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

def initDB() :
    """
    Initialisation of the database.
    """
    db.create_all()
    
    db.session.commit()


app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)

#Database part :
db = SQLAlchemy(app)

#Socket parts :
socketio = SocketIO(app)

from application import routes
from application import models

initDB()