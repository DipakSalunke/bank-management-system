from security import token_required
from flask_restful import Resource
from flask import request
import requests
import copy
from models.account import AccountModel
import logging
from schemas.account import AccountSchema, AccountCheckSchema, UserCheckSchema
import json
from marshmallow import ValidationError

logging.basicConfig(
    filename="./src/account_service/account.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s "
    + __name__
    + " %(threadName)s : %(message)s",
)
log = logging.getLogger("account_log")

BLANK_ERROR = "'{}' cannot be blank."
ACCOUNT_NOT_FOUND = "Account not found"
USERNAME_EXISTS = "username exists insert acceppted"
USER_NOT_FOUND = "user is not present, register first!"
USER_SERVICE_DOWN = "User service is not working try after some time"
USER_SERVICE_IS_PRESENT_URL = "http://127.0.0.1:5001/user/ispresent"

account_schema = AccountSchema()
accountcheck_schema = AccountCheckSchema()
usercheck_schema = UserCheckSchema()


class Account(Resource):
    @classmethod
    @token_required
    def get(cls):
        data = usercheck_schema.load(request.get_json())
        log.info("username :%s", data)
        acc = AccountModel.find_by_username(data["username"])
        log.info("get account :%s", acc)
        if acc:
            return account_schema.dump(acc), 200
        return {"message": ACCOUNT_NOT_FOUND}, 400

    @token_required
    def put(self):
        account = account_schema.load(request.get_json())
        acc = AccountModel.find_by_username(account.username)
        acc_before = copy.deepcopy(acc)
        auth_token = request.headers.get("Authorization", "")

        if acc is None:
            response = self.check_for_user(account.username, auth_token)
            log.info("check for user :%s", response)
            if response.json()["is_present"]:
                message = USERNAME_EXISTS
                log.info("account saved to db :%s", acc)
                account.save_to_db()
            else:
                return {"message": USER_NOT_FOUND}, 400

            return {"message": message, "inserted": account_schema.dump(account)}, 201
        else:
            account.save_to_db()
            return (
                {
                    "before": account_schema.dump(acc_before),
                    "updated": account_schema.dump(account),
                },
                201,
            )

    @classmethod
    def check_for_user(cls, username, auth_token: str):
        try:
            url = USER_SERVICE_IS_PRESENT_URL
            response = requests.post(
                url,
                data=json.dumps({"username": username}),
                headers={
                    "Authorization": auth_token,
                    "Content-type": "application/json",
                },
            )
        except Exception:
            log.critical("account service is down")
            response = USER_SERVICE_DOWN, 500
        return response


class AccountCheck(Resource):
    @classmethod
    @token_required
    def post(cls):
        data = accountcheck_schema.load(request.get_json())
        log.info("id to be cheked :%s", data)
        account = AccountModel.find_by_id(data["acc_id"])
        if account:
            return {"is_present": True, "username": account.username}, 200
        else:
            return {"is_present": False}, 400
