from app import db
from app.Models import *

class CommandController: 
    @classmethod
    def new(cls, data, slug): 
        u = db.session.query(User).filter(User.slug == slug).first()
        if (not u):
            return {"status": False, "data":{"error": "user not found"}}
        try:
            c = Command()
            c.name = data['name']
            if ('description' in data):
                c.description = data['description']
            c.owner = u.id
            db.session.add(c)
            db.session.commit()
            cua = Command_User_Assigment()
            cua.command_id = c.id
            cua.user_id = u.id
            if ('slug' in data):
                c.set_slug(data['slug'])
            else:
                c.set_slug()
            db.session.add(c)
            db.session.add(cua)
            db.session.commit()
            return {"status": True, "data":{"slug": c.slug}}
        except:
            return {"status": False, "data":{"error": "Something wrong"}}
    
    @classmethod
    def get(cls, cslug, uslug = False):
        if (not uslug):
            c = db.session.query(Command).filter(Command.slug == cslug).first()
            if (not c):
                return {"status": False, "data":{"error": "command not found"}}
            return {"status": True, "data": c.getInfo()}
        result = cls.checkUserInCommand(cslug, uslug)
        if (not result["status"]):
            return result
        result["data"] = result["data"]["command"].getInfo()    
        return result

    @classmethod
    def checkUserInCommand(cls, cslug, uslug):
        c = db.session.query(Command).filter(Command.slug == cslug).first()
        if (not c):
            return {"status": False, "data":{"error": "command not found"}}
        u = db.session.query(User).filter(User.slug == uslug).first()
        if (not u):
            return {"status": False, "data":{"error": "user not found"}}
        if (db.session.query(Command_User_Assigment).filter_by(command_id = c.id, user_id = u.id).first()):
            return {"status": True, "data":{"command": c, "user": u}, "edit" : True}
        return {"status": True, "data":{"command": c, "user": u}}
    