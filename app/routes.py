from logging import log
from app import app, db
from app.models import User
from flask import  session, request


@app.route('/')
def hello_world():
    if 'role' in session:
        return session['role']
    else:
        session['role'] = 'admin'
        return "unknow"

@app.route('/api/v1/auth', methods = ['POST'])
def auth():
    login = request.form['login']
    password = request.form['password']
    # DB: Auth user
    u = db.session.query(User).filter(User.username == login).first()
    if (not u):
        return "ERROR:User not found"
    if (not u.check_password(password)):
        return "ERROR:Incorrect password"
    #END DB
    return login

@app.route('/api/v1/register_company', methods = ['POST'])
def register_company():
    login = request.form['login']
    password = request.form['password']
    # DB: Set as Company
    u = User()
    u.username = login
    u.set_password(password)
    u.role = 1
    db.session.add(u)
    db.session.commit()
    #END DB
    session['login'] = login
    session['role'] = 'company'
    return login