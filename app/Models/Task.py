from app import db
from datetime import datetime

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

class User_Status_Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    candidate_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    status_goals = db.Column(db.Integer)
    progress = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    status =  db.Column(db.String(30))