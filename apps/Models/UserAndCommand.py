from werkzeug.security import generate_password_hash, check_password_hash
from apps import db
from datetime import datetime

# Здесь таблица мерджа
user_command_merge = db.Table('user_command_merge', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('command_id', db.Integer, db.ForeignKey('commands.id'))
)

class User(db.Model):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key = True)
    slug = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(64), index = True, unique = True)
    name  = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    skills = db.Column(db.String(64))
    password = db.Column(db.String(128))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    commands = db.relationship( "Command", secondary=user_command_merge, back_populates="users")
    
    def set_slug(self, user_slug = False):
        if (not user_slug):
            self.slug = "id{}".format(self.id)
            return self.slug
        if (not db.session.query(User).filter(User.slug == user_slug ).first()):
            self.slug = user_slug
            return self.slug
        return False
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def get_slug(self):
        return '{}'.format(self.slug)
    def __repr__(self):
        return '{}'.format(self.slug)


class Command(db.Model):
    __tablename__ = 'commands' 

    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime(), default=datetime.utcnow)
    companyName = db.Column(db.String(120), index = True)
    commandName = db.Column(db.String(120), index = True)
    slug = db.Column(db.String(120), index = True, unique = True)
    description = db.Column(db.Text)
    site = db.Column(db.String(120), index = True)
    owner = db.Column(db.Integer)
    users = db.relationship( "User", secondary=user_command_merge, back_populates="commands")

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