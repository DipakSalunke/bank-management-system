import requests
from blacklist import BLACKLIST
from flask import Response,request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_restful import Resource, reqparse
from models.account import AccountModel
from models.user import UserModel
from werkzeug.security import safe_str_cmp

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True, type=str,
                          help='username cannot be blank')
_user_parser.add_argument('password', required=True, type=str,
                          help='password field cannot be blank')


class CustRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username', required=True, type=str,
                        help='username cant be blank')
    parser.add_argument('password', required=True, type=str,
                        help='password field cannot be blank')
    parser.add_argument('name', required=True, type=str,
                        help='name cannot be blank')
    parser.add_argument('address', required=True, type=str,
                        help='address cannot be blank')
    parser.add_argument('state', required=True, type=str,
                        help='state cannot be blank')
    parser.add_argument('country', required=True, type=str,
                        help='country cannot be blank')
    parser.add_argument('email', required=True, type=str,
                        help='email cannot be blank')
    parser.add_argument('pan', required=True, type=str,
                        help='pan cannot be blank')
    parser.add_argument('contact', required=True, type=str,
                        help='contact field cannot be blank')
    parser.add_argument('dob', required=True, type=str,
                        help='dob cannot be blank')
    parser.add_argument('acc_type', required=True, type=str,
                        help='account type cannot be blank')

    def post(self):
        """registers a new user as well creates account for the same

        Returns:
            tuple: message, status_code
        """
        data = CustRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(data["username"], data["password"])
        user.save_to_db()
        return {"message": "User created successfully", "account_call": self.save_to_acc(data)}, 201

    def save_to_acc(self, data):
        """sends post request to save account information to the Account service

        Args:
            data (Account): Account model data

        Returns:
            tuple: message and return code
        """
        account = AccountModel(data["username"], data["name"], data["address"], data["state"],
                               data["country"], data["email"], data["pan"], data["contact"], data["dob"], data["acc_type"])
        auth_token = request.headers.get('Authorization', '')
        message = ''
        try:
            url = 'http://127.0.0.1:5002/account'
            response = requests.put(url, data=account.json(),headers={'Authorization':auth_token})
            print(response.json())
            message = "account created successfully!"
        except Exception:
            message = "Account service is not working try after some time"

        return {"message": message}, 201


class UserRegister(Resource):

    def post(self):
        """registers a new user in the system

        Returns:
            tuple: message and error code
        """
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(data["username"], data["password"])
        user.save_to_db()
        return {"message": "User created successfully"}, 201


class UserCheck(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username', required=True, type=str,
                        help='username cannot be blank')

    @jwt_required()
    def post(self):
        """checks if username is present in the db

        Returns:
            tuple: message if present or not and return status code
        """
        data = UserCheck.parser.parse_args()
        print(data['username'])
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"is_present": True}, 200
        else:
            return {"is_present": False}, 400


class User(Resource):

    @classmethod
    @jwt_required(fresh=True)
    def get(cls, user_id):
        """get the user information of the given user id

        Args:
            user_id (int): user_id

        Returns:
            User: user details
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json(), 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, user_id):
        """deletes user with provided user ID

        Args:
            user_id (int): users ID

        Returns:
            tuple: message nad status code
        """
        claims = get_jwt()
        print(claims)
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, 404

        if user.id == 1:
            return {"message": "admin can't be deleted"}, 400

        user.delete_from_db()

        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """logs in user with valid username and password and password

        Returns:
            tuple: message and status code
        """
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401

    @classmethod
    @jwt_required()
    def get(cls):
        """a authenticator for the jwt token sent for authentication by other services 
        """
        pass


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        """logs the user out of the system by blacklisting the access token

        Returns:
            tuple : message and status code
        """
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """generates fresh token for the critical endpoint

        Returns:
            tuple: message and status code
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
