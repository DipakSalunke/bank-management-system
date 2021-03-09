from flask_restful import Resource,reqparse

from models.user import UserModel
from models.account import AccountModel

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    
    parser.add_argument('username', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('password', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('name', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('address', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('state', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('country', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('email', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('pan', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('contact', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('dob', required=True, type=str, help='this field cannot be blank')
    parser.add_argument('acc_type', required=True, type=str, help='this field cannot be blank')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"A user with that username already exists"},400
        user = UserModel(data["username"],data["password"])
        account = AccountModel(data["username"],data["name"],data["address"],data["state"],data["country"],data["email"],data["pan"],data["contact"],data["dob"],data["acc_type"])
        user.save_to_db()
        account.save_to_db()
        return {"message":"User created successfully"},201

