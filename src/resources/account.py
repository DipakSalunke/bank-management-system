from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.account import AccountModel

class Account(Resource):
    
    parser = reqparse.RequestParser()
    
    parser.add_argument('username', required=True, type=str, help='username cannot be blank')
    parser.add_argument('name', required=True, type=str, help='name cannot be blank')
    parser.add_argument('address', required=True, type=str, help='address cannot be blank')
    parser.add_argument('state', required=True, type=str, help='state cannot be blank')
    parser.add_argument('country', required=True, type=str, help='country cannot be blank')
    parser.add_argument('email', required=True, type=str, help='email cannot be blank')
    parser.add_argument('pan', required=True, type=str, help='pan cannot be blank')
    parser.add_argument('contact', required=True, type=str, help='contact field cannot be blank')
    parser.add_argument('dob', required=True, type=str, help='date of birth cannot be blank')
    parser.add_argument('acc_type', required=True, type=str, help='account type cannot be blank')
    
    @jwt_required()
    def get(self):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('username', required=True, type=str, help='username cannot be blank')
        data = parser1.parse_args()
        acc = AccountModel.find_by_username(data["username"])
        if acc:
            return acc.json(),200
        return {'message':'Account not found'},400
    
    @jwt_required()
    def put(self):
        data = Account.parser.parse_args()
        acc = AccountModel.find_by_username(data["username"])
        if acc is None:
            return {'message':'Account not found'},400
        else:
            acc.name = data["name"]
            acc.address = data["address"]
            acc.state = data["state"]
            acc.country = data["country"]
            acc.email = data["email"]
            acc.pan = data["pan"]
            acc.contact = data["contact"]
            acc.dob = data["dob"]
            acc.acc_type = data["acc_type"]
        acc.save_to_db()
        
        return acc.json(),201