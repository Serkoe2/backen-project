from app import  db
from datetime import datetime

class Command_User_Assigment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    command_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    
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
            return self.slug
        return False