import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # create database instance

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app import models
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
