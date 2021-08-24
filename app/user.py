from app import db
from app.models import User

def find(data):
    if ("email" in data and 'phone' in data):
        u = db.session.query(User).filter(User.email == data['email'] or User.phone == data['phone']).first()
    elif ("email" in data):
        u = db.session.query(User).filter(User.email == data['email']).first()
    elif ("phone" in data):
        u = db.session.query(User).filter(User.phone == data['phone']).first()
    else:
        return False
    return u

def new(data): 
    if ( find(data) ):
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

def auth(data):
    try:
        u = find(data)
        if (not u):
            return {"status": False, "data": "User not found"}
        if (not u.check_password(data['password'])):
            return {"status": False, "data": "Incorrect password"}
        return {"status": True, "data":{"slug": u.slug, "role": u.role}}
    except:
        return {"status":False, "data":"Server error. Connect to administrator"}

def get(slug):
    try:
        u = db.session.query(User).filter(User.slug == slug).first()
        if (not u):
            return {"status": False, "data": {"error" : "user not found"}}
        return {"status": True, "data": u.getInfo()}
    except:
       return {"status":False, "data": {"error" : "Server error. Connect to administrator"}}

def update(slug, data):
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
            if (not find({"email": data["email"]})):
                u.email = data["email"]
            else:
                response["email_error"]= "email is forbidden"
        if ("phone" in data and editSecure):
            if (not find({"phone": data["phone"]})):
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
