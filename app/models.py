from enum import Flag
from sqlalchemy.sql.elements import Null
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

ROLE_USER = 'candidate'
ROLE_HR = 'hr'

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    slug = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(64), index = True, unique = True)
    name  = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    skills = db.Column(db.String(64))
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    password_hash = db.Column(db.String(128))
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    
    def set_slug(self, user_slug = False):
        if (not user_slug):
            self.slug = "id{}".format(self.id)
            return self.slug
        if (not db.session.query(User).filter(User.slug == user_slug ).first()):
            self.slug = user_slug
            return self.slug
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def getInfo(self):
        return {"email": self.email,"phone": self.phone, "name": self.name, "surname": self.surname,
                "role": self.role, "slug" : self.slug}
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    name = db.Column(db.String(120), index = True)
    description = db.Column(db.Text)
    tasks = db.relationship('Task', backref='company')

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
    parent_Task = db.Column(db.Integer, db.ForeignKey('task.id'))

class User_Status_Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    candidate_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    status_goals = db.Column(db.Integer)
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



