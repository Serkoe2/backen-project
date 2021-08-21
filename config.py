import os
print("### import config ###")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    if  os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) 
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:q@localhost:6666/GetOffer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    DEBUG = True
    SECRET_KEY = 'secret-key'

if __name__ == '__main__':
    q = Config()
    print(q.SQLALCHEMY_DATABASE_URI)
    print(basedir)

