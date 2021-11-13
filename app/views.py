from flask.json import jsonify
from app import db
import sqlalchemy
from app.Models import *
import inspect


def getUsers():
    objs = db.session.query(User).all()
    result = inspect.getmembers(User)
    fields = []
    for i in result:
        if type(i[1]) == sqlalchemy.orm.attributes.InstrumentedAttribute:
            fields.append(i[0])
    result = {"header": fields}
    data = []
    for obj in objs:
        temp = []
        for i in fields:
            temp.append(obj.__getattribute__(i))
        data.append(temp)
    result["data"] = data
    return result
    
def getCommands():
    objs = db.session.query(Command).all()
    result = inspect.getmembers(Command)
    fields = []
    for i in result:
        if type(i[1]) == sqlalchemy.orm.attributes.InstrumentedAttribute:
            fields.append(i[0])
    result = {"header": fields}
    data = []
    for obj in objs:
        temp = []
        for i in fields:
            temp.append(obj.__getattribute__(i))
        data.append(temp)
    result["data"] = data
    return result

def getCommand_User_Assigment():
    objs = db.session.query(Command_User_Assigment).all()
    result = inspect.getmembers(Command_User_Assigment)
    fields = []
    for i in result:
        if type(i[1]) == sqlalchemy.orm.attributes.InstrumentedAttribute:
            fields.append(i[0])
    result = {"header": fields}
    data = []
    for obj in objs:
        temp = []
        for i in fields:
            temp.append(obj.__getattribute__(i))
        data.append(temp)
    result["data"] = data
    return result

def getTasks():
    objs = db.session.query(Task).all()
    result = inspect.getmembers(Task)
    fields = []
    for i in result:
        if type(i[1]) == sqlalchemy.orm.attributes.InstrumentedAttribute:
            fields.append(i[0])
    result = {"header": fields}
    data = []
    for obj in objs:
        temp = []
        for i in fields:
            temp.append(obj.__getattribute__(i))
        data.append(temp)
    result["data"] = data
    return result