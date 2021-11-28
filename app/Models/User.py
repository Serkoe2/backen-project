from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    slug = db.Column(db.String(120), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(64), index = True, unique = True)
    name  = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    skills = db.Column(db.String(64))
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