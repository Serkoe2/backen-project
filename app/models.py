from enum import Flag
from sqlalchemy.sql.elements import Null
from werkzeug.security import generate_password_hash, check_password_hash
from app import command, db
from datetime import datetime

ROLE_USER = 'candidate'
ROLE_HR = 'hr'
GRADES = ['junior','middle','senior']

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
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Command(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    name = db.Column(db.String(120), index = True)
    slug = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.Text)
    owner = db.Column(db.Integer)
    def getInfo(self):
        return {"name": self.name,"description": self.description,  "slug" : self.slug, "owner": self.owner}
    def set_slug(self, command_slug = False):
        if (not command_slug):
            self.slug = "id{}".format(self.id)
            return self.slug
        if (not db.session.query(Command).filter(Command.slug == command_slug ).first()):
            self.slug = command_slug
            return self.command_slug
        return False

class Command_User_Assigment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    command_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

# Сущность, которая явяется родительской ссылкой для Целей(Goal)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    grade = db.Column(db.String(30))
    description = db.Column(db.Text)
    command = db.Column(db.Integer, index = True)
    owner = db.Column(db.Integer)
    created = db.Column(db.DateTime(), default=datetime.utcnow)

    def getInfo(self):
        return {"id":self.id, "name":self.name, "grade": self.grade, "description": self.description, "created":self.created}

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(120))
    description = db.Column(db.Text)

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



