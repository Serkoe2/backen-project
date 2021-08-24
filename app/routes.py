from logging import log
import re
from app import app, db, user
from app.models import User, Company
from flask import  session, request, jsonify


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

# ----------------------------------Устаревшие методы ----------------------------------
# регистрация компании
@app.route('/api/v1/addNewCompany', methods = ['POST'])
def register_company():
    if (not request.is_json):
        return "ERROR:DATA is not JSON"
    data = request.json
    if (not "name" in data or not "description" in data):
        return "ERROR:DATA is not correct format"
    c = Company()
    c.name = data['name']
    c.description = data['description']
    return "OK"

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