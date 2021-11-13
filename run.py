from app import app, db
from app.Models.User import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}