from security import token_required
from flask_restful import Resource, reqparse
from flask import request
import requests
import copy
from models.account import AccountModel
import logging

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


class Account(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        "username", required=True, type=str, help=BLANK_ERROR.format("username")
    )
    parser.add_argument(
        "name", required=True, type=str, help=BLANK_ERROR.format("name")
    )
    parser.add_argument("address", required=True, type=str, help=BLANK_ERROR)
    parser.add_argument(
        "state", required=True, type=str, help=BLANK_ERROR.format("state")
    )
    parser.add_argument(
        "country", required=True, type=str, help=BLANK_ERROR.format("country")
    )
    parser.add_argument(
        "email", required=True, type=str, help=BLANK_ERROR.format("email")
    )
    parser.add_argument("pan", required=True, type=str, help=BLANK_ERROR.format("pan"))
    parser.add_argument(
        "contact", required=True, type=str, help=BLANK_ERROR.format("contact")
    )
    parser.add_argument(
        "dob", required=True, type=str, help=BLANK_ERROR.format("birthdate")
    )
    parser.add_argument(
        "acc_type", required=True, type=str, help=BLANK_ERROR.format("account type")
    )

    @classmethod
    @token_required
    def get(cls):
        parser1 = reqparse.RequestParser()
        parser1.add_argument("username", required=True, type=str, help=BLANK_ERROR)
        data = parser1.parse_args()
        log.info("username :%s", data)
        acc = AccountModel.find_by_username(data["username"])
        log.info("get account :%s", acc)
        if acc:
            return acc.json(), 200
        return {"message": ACCOUNT_NOT_FOUND}, 400

    @token_required
    def put(self):
        data = Account.parser.parse_args()
        acc = AccountModel.find_by_username(data["username"])
        acc_before = copy.deepcopy(acc)
        auth_token = request.headers.get("Authorization", "")

        if acc is None:
            response = self.check_for_user(data, auth_token)
            log.info("check for user :%s", response)
            if response.json()["is_present"]:
                message = USERNAME_EXISTS
                acc = AccountModel(**data)
                log.info("account saved to db :%s", acc)
                acc.save_to_db()
            else:
                return {"message": USER_NOT_FOUND}, 400

            return {"message": message, "inserted": acc.json()}, 201
        else:
            acc = AccountModel(**data)
            acc.save_to_db()
            return {"before": acc_before.json(), "updated": acc.json()}, 201

    @classmethod
    def check_for_user(cls, data, auth_token: str):
        try:
            url = USER_SERVICE_IS_PRESENT_URL
            response = requests.post(
                url,
                data={"username": data["username"]},
                headers={"Authorization": auth_token},
            )
        except Exception:
            log.critical("account service is down")
            response = USER_SERVICE_DOWN, 500
        return response


class AccountCheck(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        "acc_id", required=True, type=str, help=BLANK_ERROR.format("account id")
    )

    @classmethod
    @token_required
    def post(cls):
        data = AccountCheck.parser.parse_args()
        log.info("id to be cheked :%s", data)
        account = AccountModel.find_by_id(data["acc_id"])
        if account:
            return {"is_present": True, "username": account.username}, 200
        else:
            return {"is_present": False}, 400
