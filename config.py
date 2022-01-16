import os
from dotenv import load_dotenv
print("### import config ###")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    if not os.getenv("ENVIROMENT"):
        load_dotenv('.env')
    if (os.environ.get('POSTGRES_HOST')):
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@postgres:5432/postgres".format(
        os.environ.get('POSTGRES_USERNAME'),
        os.environ.get('POSTGRES_PASSWORD'))
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://starter_kit:qwerty@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
    DEBUG = True
    SECRET_KEY = 'secret-key'