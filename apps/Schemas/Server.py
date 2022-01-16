from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from dataclasses import dataclass

class ResponseSchema(Schema):
    """
    Общий стандарт ответа от сервера
    """
    status: bool = fields.Boolean()
    error_msg: str = fields.Str()
    data: dict = fields.Dict()