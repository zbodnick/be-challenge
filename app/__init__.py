from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name]) 

    db.init_app(app)

    from app.lighters.routes import bp as l_bp
    from app.manufacturers.routes import bp as m_bp

    # register blueprint modules
    app.register_blueprint(l_bp, url_prefix='/lighters')
    app.register_blueprint(m_bp, url_prefix='/manufacturers')

    return app