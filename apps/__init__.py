import os
from flask import Flask
from flask_cors import CORS
from importlib import import_module
from apps.Mailer import Mailer


from flask_sqlalchemy import SQLAlchemy

mailer = Mailer(
    os.getenv("SMTP_SERVER"),
    os.getenv("SMTP_PORT"),
    os.getenv("SMTP_LOGIN"),
    os.getenv("SMTP_PASSWORD")
)
db = SQLAlchemy()

def register_extensions(app: Flask) -> None:
    """
    Регистрирует все расширения
    """
    CORS().init_app(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def register_blueprints(app: Flask) -> None:
    """
    Регистрирует все приложения
    """
    for module_name in ('user', 'social', 'command'):
        module = import_module('apps.Api.{}'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(config: object) -> Flask:
    """
    Создает и возвращает Flask приложение
    """
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    register_extensions(app)
    configure_database(app)
    return app
