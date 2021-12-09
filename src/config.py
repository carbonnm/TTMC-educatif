import os
import binascii

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    """
    Configuration class.
    """
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    #track the modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = True