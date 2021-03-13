from ma import ma
from models.loan import LoanModel
from marshmallow import fields


class LoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LoanModel
        dump_only = (
            "id",
            "date",
        )
        load_instance = True


class AccountCheckSchema(ma.Schema):
    acc_id = fields.Int(required=True)
