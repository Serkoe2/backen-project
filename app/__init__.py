import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.Mailer import Mailer


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mailer(
    os.getenv("SMTP_SERVER"),
    os.getenv("SMTP_PORT"),
    os.getenv("SMTP_LOGIN"),
    os.getenv("SMTP_PASSWORD"))
if app.debug:
    print(app.config)

from app import routes

