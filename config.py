import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False

class Dev(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lighter_collection.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Test(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lighter_collection.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Prod(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lighter_collection.db')
    DEBUG = False

config_by_name = dict(
    dev=Dev,
    test=Test,
    prod=Prod
)