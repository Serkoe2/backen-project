from logging import error
from app import db
from app import command
from app.models import Task, Command, GRADES

def new(data):
    result = command.checkUserInCommand(data['command_slug'],data['user'])
    if ('edit' not in result):
        return {"status": "false", data: { "error": "forbidden"}}
    t = Task()
    t.name = data['name']
    if ('grade' in data):
        t.grade = data['grade']
    if ('description' in data):
        t.grade = data['description']
    t.command = result["data"]["command"].id
    t.owner = result["data"]["user"].id
    try:
        db.session.add(t)
        db.session.commit()
        return {"status": True, "data":{"id": t.id}}
    except:
        return {"status": False, "data":{"error": "Something wrong"}}

def all(data):
    c = db.session.query(Command).filter(Command.slug == data["command_slug"]).first()
    if (not c):
        return {"status": False, "data":{"error": "command not found"}}
    tasks = db.session.query(Task).filter(Task.command == c.id).all()
    data = []
    for i in tasks:
        data.append(i.getInfo())
    return data

def get(data):
    t = db.session.query(Task).filter_by(command = check['data']['command'].id, id = data["task_id"]).first()
    if (not t):
        return {"status": "false", data: { "error": "task not found"}}

    return {"status": True, "data":t.getIngo()}

def update(data):
    check = command.checkUserInCommand(data['command_slug'],data['user'])
    if (not check["status"]):
        return check
    if ('edit' not in check):
        return {"status": "false", data: { "error": "forbidden"}}
    t = db.session.query(Task).filter_by(command = check['data']['command'].id, id = data["task_id"]).first()
    if (not t):
        return {"status": "false", data: { "error": "task not found"}}
    errors = {}
    if ("name" in data and data["name"] != ''):
        t.name = data["name"]
    if ("description" in data):
        t.description = data["description"]
    if ("grade" in data):
        if (data["grade"] not in GRADES):
            errors["grade"] = "{} is not valid grade".format(data["grade"])
        else:
            t.grade = data["grade"]
    try:
        db.session.add(t)
        db.session.commit()
        return {"status": True, "data": errors }
    except:
        return {"status": False, "data":{"error": "Something wrong"}}
    