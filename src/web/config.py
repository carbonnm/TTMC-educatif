import os
import binascii

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    """
    Configuration class.
    Initialisation of the environnement configuration.
    Parameters :
    --------------
    object : str 
    """
    DEBUG = True
    ENV = 'development'
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    #track the modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = True