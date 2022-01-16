from logging import error
from apps import mailer, db
from flask import  session, request, Blueprint
from apps.Models import User
from apps.Schemas import ResponseSchema, UserCredSchema

blueprint = Blueprint( 'user_blueprint', __name__, url_prefix='/api/v1/user')
@blueprint.route('/')
def hello_world():
    if 'role' in session:
        return "session['role']"
    else:
        session['role'] = 'admin1'
        return "unknow"

@blueprint.route("/test_mailer", methods = ['POST'])
def test_mailer():
    from random import randint
    to = request.json["to"]
    data = {"url": "https://google.com", "code": str(randint(1000, 9999))}
    template_path = "template2.html"
    mailer.send(to, "Get Offer", template_path, data)
    return "OK"

# Регистрация
@blueprint.route('/new', methods = ['POST'])
def new_user():
    errors = UserCredSchema().validate(request.json)
    if errors:
        return ResponseSchema().dumps({"status": False, "error_msg": errors})
    if (db.session.query(User).filter(User.email == request.json["email"]).first()):
        return ResponseSchema().dumps({"status": False, "error_msg": "Email already use"})
    user = User()
    user.email = request.json["email"]
    user.set_password(request.json["password"])
    db.session.add(user)
    db.session.commit()
    user.set_slug()
    db.session.add(user)
    db.session.commit()
    session['slug'] = user.slug
    response = {'status': True, 'data': {'slug': user.slug}, 'error_msg': ''}
    return ResponseSchema().dumps(response)

# Авторизация
@blueprint.route('/auth', methods = ['POST'])
def auth_user():
    errors = UserCredSchema().validate(request.json)
    if errors:
        return ResponseSchema().dumps({"status": False, "error_msg": errors})
    user = db.session.query(User).filter(User.email == request.json["email"]).first()
    if (not user or not user.check_password(request.json["password"])):
        return ResponseSchema().dumps({"status": False, "error_msg": "User or Password is not correct"})
    
    session['slug'] = user.slug
    response = {'status': True, 'data': {'slug': user.slug}, 'error_msg': ''}
    return ResponseSchema().dumps(response)

# Информация о пользователе
@blueprint.route('/get/<slug>', methods = ['POST'])
def get_user(slug):
    user = db.session.query(User).filter(User.slug == slug).first()
    if (not user):
        return ResponseSchema().dumps({"status": False, "error_msg": "User not found"})
    response = {'status': True, 'data': {'slug': user.slug, 'email': user.email}, 'error_msg': ''}
    if ('slug' in session and slug == session['slug']):
        response['data']['edit'] = True
    return ResponseSchema().dumps(response)