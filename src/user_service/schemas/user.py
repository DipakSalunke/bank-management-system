from ma import ma
from models.user import UserModel
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True


class UserCheckSchema(ma.Schema):
    username = fields.Str(required=True)
