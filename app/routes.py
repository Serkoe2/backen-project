from logging import log
import re
import json
from app import app, command, user, task, views
from flask import  session, request, jsonify, render_template, redirect
from . import Autorize


@app.route('/')
def hello_world():
    if 'role' in session:
        return session['role']
    else:
        session['role'] = 'admin'
        return "unknow"

# Если мне передадут пользователей с пустыми строками??
# Регистрация
@app.route('/api/v1/user/new', methods = ['POST'])
def new_user():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ('email' not in request.json):
        return jsonify({"status":False, "data": {"error": "No email"}})
    if ('password' not in request.json):
        return jsonify({"status":False, "data": {"error": "No password"}})
    result = user.new(request.json)
    print(result)
    if (not result["status"]):
        return jsonify(result)
    session['slug'] = result["data"]["slug"]
    session['role'] = 'candidate'
    return 'OK'

# Авторизация
# Нуже валидатор
@app.route('/api/v1/user/auth', methods = ['POST'])
def auth():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ('email' not in request.json and 'phone' not in request.json):
        return jsonify({"status":False, "data": {"error": "No email or phone"}})
    if ('password' not in request.json):
        return jsonify({"status":False, "data": {"error": "No password"}})
    result = user.auth(request.json)
    if (not result["status"]):
        return jsonify(result)
    session['slug'] = result["data"]["slug"]
    session['role'] = result["data"]["role"]
    return "OK"

@app.route('/api/v1/user/get/<slug>', methods = ['POST'])
def userGet(slug):
    result = user.get(slug)
    if ("slug" in session and session["slug"] == slug):
        result["edit"] = True
    return jsonify(result)

@app.route('/api/v1/user/update', methods = ['POST'])
def userUpdate():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "data is not JSON"}})
    if ("slug" not in session):
        return jsonify({"status":False, "data": {"error": "Non auth user"}})
    result = user.update(session["slug"], request.json)
    return jsonify(result)

@app.route('/api/v1/command/new', methods = ['POST'])
def new_command():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ("slug" not in session):
        return jsonify({"status":False, "data": {"error": "Non auth user"}})
    if ('name' not in request.json or request.json['name'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid name"}})

    result = command.new(request.json,session['slug'])
    if (not result["status"]):
        return jsonify(result)
    session['role'] = 'command'
    return jsonify(result)

@app.route('/api/v1/command/get/<slug>', methods = ['POST'])
def commandGet(slug):
    if (slug == ''):
        return jsonify({"status":False, "data": {"error": "invalid name"}})
    if ('slug' in session):
        result = command.get(slug, session['slug'])
    else:
        result = command.get(slug)
    return jsonify(result)

@app.route('/api/v1/task/new', methods = ['POST'])
def taskNew():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ("slug" not in session):
        return jsonify({"status":False, "data": {"error": "Non auth user"}})
    if ('name' not in request.json or request.json['name'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid name"}})
    if ('command_slug' not in request.json or request.json['command_slug'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid command"}})

    request.json["user"] = session["slug"]
    result = task.new(request.json)
    return jsonify(result)

@app.route('/api/v1/task/all', methods = ['POST'])
def taskAll():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ('command_slug' not in request.json or request.json['command_slug'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid command"}})

    result = task.all(request.json)
    return jsonify(result)

@app.route('/api/v1/task/get', methods = ['POST'])
def taskGet():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ('command_slug' not in request.json or request.json['command_slug'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid command"}})
    if ("task_id" not in request.json):
        return jsonify({"status":False, "data": {"error": "invalid task id"}})
    
    result = task.get(request.json)
    return jsonify(result)

@app.route('/api/v1/task/update', methods = ['POST'])
def taskUpdate():
    if (not request.is_json):
        return jsonify({"status":False, "data": {"error": "Data is not JSON"}})
    if ("slug" not in session):
        return jsonify({"status":False, "data": {"error": "Non auth user"}})
    if ("command_slug" not in request.json or request.json['command_slug'] == ''):
        return jsonify({"status":False, "data": {"error": "invalid command"}})
    if ("task_id" not in request.json):
        return jsonify({"status":False, "data": {"error": "invalid task id"}})

    request.json['user'] = session['slug']
    result = task.update(request.json)
    return jsonify(result)

# ----------------------------------Админка методы ----------------------------------
@app.route('/c9OXvzWc281bXK0xohPv/<table>', methods = ['GET','POST'])
def getTable(table):
    if (request.method == 'GET'):
        return render_template('views.html')
    if (request.method == 'POST'):
        if (table == "user"):
            result = views.getUsers()
        elif (table == "command"):
            result = views.getCommands()
        elif (table == "task"):
            result = views.getTasks()
        elif (table == "cus"):
            result = views.getCommand_User_Assigment()

        return jsonify(result)

# ----------------------------------Тест методы ----------------------------------
@app.route('/auth_google')
def test_auth():
    #return redirect(google_auth.get_auth_url())
    return redirect(Autorize.Google.get_auth_url())

@app.route('/test', methods = ['GET','POST'])
def handler_redirect():
    code = request.args.get('code')
    data = Autorize.Google.get_token_url(code)
    info = Autorize.Google.get_info_url(data["access_token"], data["id_token"])
    if (not info):
        return jsonify({"status":False, "data": {"error": "Auth failed"}})
    return jsonify(info)

# ----------------------------------Устаревшие методы ----------------------------------

# Создать новую таску или апдейт старой
# Принимаемые данные JSON
# task_id - id родительского таска
# Если параметра нет, автоматически будет создан новый task
# Для создания новой цели goals не должен быть пустым
# Goals - массив целей
# subject - задача цели
# decription - описание цели
# пример создания нового таска:
# {goals: [{subject: "TEST" , description:"test test test"}]}
# В случае успеха возвращает id
@app.route('/api/v1/addNewGoal', methods = ['POST'])
def addNewGoal():
    #принять аргументы json
    if (not request.is_json):
        return "ERROR:DATA is not JSON"
    data = request.json
    if (not "task" in data or not "goals" in data):
        return "ERROR:DATA is not correct format"
    # добавление goal в task
    if ("id" in data['task']):
        return "future"
    # создание цели
    
    return "OK"