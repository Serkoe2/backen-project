from flask.json import jsonify
from marshmallow.fields import Method
from apps import  db
from flask import  session, request, Blueprint, render_template, redirect
from apps.Models import User
from apps.Schemas import ( 
    ResponseSchema,
    SocialData
)
from apps.Social import Autorize

blueprint = Blueprint( 'social_blueprint', __name__, url_prefix='/api/v1/social')
authorizer = Autorize()

@blueprint.route('/')
def hello_world():
    return render_template('index.html')

@blueprint.route('/google', methods=["GET"])
def google():
    return redirect(authorizer.Google.user_redirect_uri)

@blueprint.route('/handler/<service>', methods=["GET"])
def handler(service):
    args = request.args
    if (service == "google"):
        if 'code' not in args:
            return ResponseSchema().dumps({"status": False, "error_msg": "Auth Failed"})
        data = authorizer.Google.get_token_url(args['code'])
        if (not data):
            return ResponseSchema().dumps({"status": False, "error_msg": "Auth Failed"})
        data = authorizer.Google.get_info(data['access_token'], data["id_token"])
        user = db.session.query(User).filter(User.email == request.json["email"]).first()
        if (not user):
            user = reg_user_google(data)
        session['slug'] = user.slug
        return redirect("/api/v1/social")


def reg_user_google(data: SocialData)->User:
    """
    Регестрируем пользователя из сервиса Google
    """
    user = User()
    user.email = data['email']
    user.name = data['given_name']
    user.surname = data['family_name']
    # Google говорит параметр verified_email
    db.session.add(user)
    db.session.commit()
    user.set_slug()
