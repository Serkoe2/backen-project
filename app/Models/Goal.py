from app import  db

class User_Status_Goals(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    goal_id = db.Column(db.Integer)
    cur_solution = db.Column(db.Text)
    status =  db.Column(db.String(30))

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(120))
    description = db.Column(db.Text)
