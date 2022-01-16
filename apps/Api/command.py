from logging.handlers import MemoryHandler
from os import name
from urllib import response
from apps import mailer, db
from flask import  session, request, Blueprint
from apps.Models import User, Command
from apps.Schemas import ResponseSchema, CommandCredSchema, AddToCommandSchema

blueprint = Blueprint( 'command_blueprint', __name__, url_prefix='/api/v1/command')

@blueprint.route('/', methods = ['POST'])
def hello_world():
    return "Command API"

# Создание команды
@blueprint.route('/new', methods = ['POST'])
def new():
    ######## Check ###########
    if not 'slug' in session:
        return ResponseSchema().dumps({"status": False, "error_msg": "User not authorized"})
    errors = CommandCredSchema().validate(request.json)
    if errors:
        return ResponseSchema().dumps({"status": False, "error_msg": errors})
    ######## End Check ###########
    c = Command()
    u = db.session.query(User).filter(User.slug == session["slug"]).first()
    c.companyName = request.json["companyName"]
    c.commandName = request.json["commandName"]
    c.site = request.json["site"]
    c.description = request.json["description"]
    c.owner = u.id
    c.users.append(u)
    db.session.add(c)
    db.session.commit()
    c.set_slug()
    db.session.add(c)
    db.session.commit()
    response = {'status': True, 'data': {'slug': c.slug}, 'error_msg': ''}
    return ResponseSchema().dumps(response)

# Получить инфо команды
# comapanyName, commandName, Description
# Если авторизован +Owner_Slug, User_Slugs
@blueprint.route('/get/<slug>', methods = ['POST'])
def getInfo(slug):
    ######## Check ###########
    c = db.session.query(Command).filter(Command.slug == slug).first()
    if not c:
        return ResponseSchema().dumps({"status": False, "error_msg": "Command not found"})
    ######## End Check ###########
    data = {
        "companyName": c.companyName,
        "commandName": c.commandName,
        "description": c.description,
        "site": c.site
    }
    members = list(map(lambda i: i.get_slug(), c.users))
    if ('slug' in session and session['slug'] in members):
        data["members"] = members
        data["owner"] = session['slug']
    response = {'status': True, 'data': data}
    return ResponseSchema().dumps(response)

# commandSlug, userSlug
@blueprint.route('/addUser', methods = ['POST'])
def addUser():
    ######## Check ###########
    if (not 'slug' in session):
        return ResponseSchema().dumps({"status": False, "error_msg": "No Authorized User"})
    errors = AddToCommandSchema().validate(request.json)
    if errors:
        return ResponseSchema().dumps({"status": False, "error_msg": errors})
    ######## End Check ###########

    u = db.session.query(User).filter(User.slug == session['slug']).first()
    if not u:
        return ResponseSchema().dumps({"status": False, "error_msg": "User not found"})
    u_add = db.session.query(User).filter(User.email == request.json['userEmail']).first()
    if not u_add:
        return ResponseSchema().dumps({"status": False, "error_msg": "Email not found"})
    print(list(map(lambda i: i.slug, u.commands)))
    if (request.json['commandSlug'] not in list(map(lambda i: i.slug, u.commands))):
        return ResponseSchema().dumps({"status": False, "error_msg": "User not have permission in this command"})
    c = db.session.query(Command).filter(Command.slug == request.json['commandSlug']).first()
    c.users.append(u_add)
    db.session.add(c)
    db.session.commit()

    return ResponseSchema().dumps({"status": True, "error_msg": ""})

# Получить все Сформированные задания команды
# Пока нет тасков
@blueprint.route('/getTask', methods = ['POST'])
def getTask():
    return "Get Task"

