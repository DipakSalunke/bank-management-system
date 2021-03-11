from security import token_required
from flask_restful import Resource, reqparse
from flask import request
import requests
import copy
from models.account import AccountModel
import logging

logging.basicConfig(filename='./src/account_service/account.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s '+__name__+' %(threadName)s : %(message)s')
log = logging.getLogger("account_log")


class Account(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username', required=True, type=str,
                        help='username cannot be blank')
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
                        help='date of birth cannot be blank')
    parser.add_argument('acc_type', required=True, type=str,
                        help='account type cannot be blank')

    @token_required
    def get(self):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('username', required=True,
                             type=str, help='username cannot be blank')
        data = parser1.parse_args()
        log.info("username :%s",data)
        acc = AccountModel.find_by_username(data["username"])
        log.info("get account :%s",acc)
        if acc:
            return acc.json(), 200
        return {'message': 'Account not found'}, 400

    @token_required
    def put(self):
        data = Account.parser.parse_args()
        acc = AccountModel.find_by_username(data["username"])
        acc_before = copy.deepcopy(acc)
        auth_token = request.headers.get('Authorization', '')

        if acc is None:
            response = self.check_for_user(data, auth_token)
            log.info("check for user :%s",response)
            if response.json()["is_present"]:
                message = "username exists insert acceppted"
                acc = AccountModel(**data)
                log.info("account saved to db :%s",acc)
                acc.save_to_db()
            else:
                return {"message": "user is not present, register first!"}, 400

            return {"message": message, "inserted": acc.json()}, 201
        else:
            acc = AccountModel(**data)
            acc.save_to_db()
            return {"before": acc_before.json(), "updated": acc.json()}, 201

    def check_for_user(self, data, auth_token):
        try:
            url = 'http://127.0.0.1:5001/user/ispresent'
            response = requests.post(url, data={"username": data["username"]}, headers={
                                     'Authorization': auth_token})
        except Exception:
            log.critical("account service is down")
            response = "User service is not working try after some time", 500
        return response


class AccountCheck(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('acc_id', required=True, type=str,
                        help='acc_id cannot be blank')

    @token_required
    def post(self):
        data = AccountCheck.parser.parse_args()
        log.info("id to be cheked :%s",data)
        account = AccountModel.find_by_id(data['acc_id'])
        if account:
            return {"is_present": True, "username": account.username}, 200
        else:
            return {"is_present": False}, 400
