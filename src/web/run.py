"""
Running of the application.
"""
from application import app
from application import socketio

if __name__ == '__main__' :
    socketio.run(app)