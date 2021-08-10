from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_COMPANY = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(64), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    password_hash = db.Column(db.String(128))
    #avatar = db.Column(db.)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    #active
    #lastlogin  
    link_info_id = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    #slug
    name = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.Text)
    tasks = db.relationship('Task', backref='company')
    #active tasks
    #completed tasks

# Сущность, которая явяется родительской ссылкой для Целей(Goal)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('company.id'))
    goals = db.relationship('Goal', backref='goals')

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(120))
    description = db.Column(db.Text)
    #assets
    #answer
    parent_Task = db.Column(db.Integer, db.ForeignKey('task.id'))

class User_Status_Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    candidate_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    status_goals = db.Column(db.Integer)
    #startime
    #endtime
    progress = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    status =  db.Column(db.String(30))

class User_Status_Goals(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    goal_id = db.Column(db.Integer)
    cur_solution = db.Column(db.Text)
    #assets
    #last_update
    status =  db.Column(db.String(30))



