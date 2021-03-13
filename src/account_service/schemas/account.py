from ma import ma
from models.account import AccountModel
from marshmallow import fields


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        dump_only = ("id",)
        load_instance = True


class AccountCheckSchema(ma.Schema):
    acc_id = fields.Int(required=True)


class UserCheckSchema(ma.Schema):
    username = fields.Str(required=True)
