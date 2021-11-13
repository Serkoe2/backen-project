from app import db
from app.Models import *

class UserController:
    @classmethod
    def find(cls, data) -> User:
        if ("email" in data and 'phone' in data):
            u = db.session.query(User).filter_by(email == data['email'], phone == data['phone']).first()
        elif ("email" in data):
            u = db.session.query(User).filter(User.email == data['email']).first()
        elif ("phone" in data):
            u = db.session.query(User).filter(User.phone == data['phone']).first()
        else:
            return False
        return u

    @classmethod
    def new(cls, data): 
        if ( cls.find(data) ):
            return {"status": False, "data":{"error": "user already register"}}
        try:
            u = User()
            if ("email" in data):
                u.email = data['email']
            if ("phone" in data):
                u.phone = data['phone']
            u.set_password(data['password'])
            u.role = 0
            db.session.add(u)
            db.session.commit()
            u.set_slug()
            db.session.add(u)
            db.session.commit()
            return {"status": True, "data":{"slug": u.slug}}
        except:
            return {"status": False, "data":{"error": "Something wrong"}}

    @classmethod
    def auth(cls, data):
        try:
            u = cls.find(data)
            if (not u):
                return {"status": False, "data": "User not found"}
            if (not u.check_password(data['password'])):
                return {"status": False, "data": "Incorrect password"}
            return {"status": True, "data":{"slug": u.slug, "role": u.role}}
        except:
            return {"status":False, "data":"Server error. Connect to administrator"}
    @classmethod
    def get(cls, slug):
        try:
            u = db.session.query(User).filter(User.slug == slug).first()
            if (not u):
                return {"status": False, "data": {"error" : "user not found"}}
            return {"status": True, "data": u.getInfo()}
        except:
            return {"status":False, "data": {"error" : "Server error. Connect to administrator"}}
    
    @classmethod
    def update(cls, slug, data):
        try:
            response = {"status": True}

            editSecure = False
            u = db.session.query(User).filter(User.slug == slug).first()
            if (not u):
                return {"status": False, "data": {"error" : "user not found"}}
            if ("name" in data):
                u.name = data["name"]
            if ("surname" in data):
                u.surname = data["surname"]
            
            #Secure section
            if ("current_password" in data and u.check_password(data["current_password"])):
                editSecure = True
            if ("email" in data and editSecure):
                if (not cls.find({"email": data["email"]})):
                    u.email = data["email"]
                else:
                    response["email_error"]= "email is forbidden"
            if ("phone" in data and editSecure):
                if (not cls.find({"phone": data["phone"]})):
                    u.phone = data["phone"]
                else:
                    response["phone_error"] = "phone is forbidden"     
            if ("password" in data and editSecure):
                u.set_password(data["password"])
            db.session.add(u)
            db.session.commit()
            return response
        except:
            return {"status":False, "data": {"error" : "Server error. Connect to administrator"}}

    @classmethod
    def delete_user(cls, u):
        db.session.delete(u)
        db.session.commit()