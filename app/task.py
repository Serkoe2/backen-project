from app import db
from app import command
from app.models import Task

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
