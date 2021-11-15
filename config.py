import os
print("### import config ###")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    if (os.environ.get('POSTGRES_HOST')):
        SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@postgres:5432/test".format(
        os.environ.get('POSTGRES_USERNAME'),
        os.environ.get('POSTGRES_PASSWORD'))
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:q@localhost:5432/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DEBUG = True
    SECRET_KEY = 'secret-key'

if __name__ == '__main__':
    q = Config()
    print(q.SQLALCHEMY_DATABASE_URI)
    print(basedir)

