from distutils import command
from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from apps.Models import User

class UserCredSchema(Schema):
    """
    Схема запроса user/new
    """
    email: str = fields.Email(validate=validate.Email(), required=True)
    password: str = fields.Str(required=True)
    phone: str = fields.Str()
    
    @post_load
    def get_user(self, data, **kwargs):
        return User(**data)

    @validates("password")
    def validate_password(self, value: str):
        if (len(value) < 2):
            raise ValidationError("Password must be longer")

class CommandCredSchema(Schema):
    """
    Схема запроса command/new
    """
    companyName: str = fields.Str(required=True)
    site: str = fields.Str(required=True)
    commandName: str = fields.Str(required=True)
    description: str = fields.Str(required=True)

class AddToCommandSchema(Schema):
    """
    Схема запроса command/addUser
    """
    commandSlug: str = fields.Str(required=True)
    userEmail: str = fields.Str(required=True)