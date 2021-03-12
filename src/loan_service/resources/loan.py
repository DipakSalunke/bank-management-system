from security import token_required
from flask_restful import Resource, reqparse
import requests
from datetime import datetime
from models.loan import LoanModel
from json import dumps
from flask import request, jsonify

import logging

logging.basicConfig(
    filename="./src/loan_service/loan.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s "
    + __name__
    + " %(threadName)s : %(message)s",
)
log = logging.getLogger("loan_log")


BLANK_ERROR = "'{}' cannot be blank."
LOAN_NOT_FOUND = "Loans not found for given account"
ACCOUNT_SERVICE_DOWN = "Account service is not working try after some time"
ACCOUNT_EXISTS = "Account exists loan acceppted"
ACCOUNT_NOT_FOUND = "You need account to get a loan, register first!"
ACCOUNT_SERVICE_IS_PRESENT_URL = "http://127.0.0.1:5002/account/ispresent"


class Loan(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "acc_id", required=True, type=str, help=BLANK_ERROR.format("account id")
    )
    parser.add_argument(
        "loan_type", required=True, type=str, help=BLANK_ERROR.format("loan type")
    )
    parser.add_argument(
        "loan_amt", required=True, type=float, help=BLANK_ERROR.format("loan ammount")
    )
    parser.add_argument(
        "rate_of_int",
        required=True,
        type=float,
        help=BLANK_ERROR.format("interest rate"),
    )
    parser.add_argument(
        "duration", required=True, type=float, help=BLANK_ERROR.format("loan duration")
    )

    @classmethod
    @token_required
    def get(cls):
        parser1 = reqparse.RequestParser()
        parser1.add_argument(
            "acc_id", required=True, type=int, help=BLANK_ERROR.format("account id")
        )
        data = parser1.parse_args()

        log.debug("acc_id: %s", data["acc_id"])

        loans = LoanModel.find_by_accid(data["acc_id"])
        loans = [loan.json() for loan in loans]

        log.debug("loans %s", loans)

        if len(loans) > 0:
            return {"loans": loans}, 200
        else:
            return {"message": LOAN_NOT_FOUND}, 404

    @token_required
    def post(self):
        data = Loan.parser.parse_args()
        loan = LoanModel(str(datetime.utcnow()), **data)
        auth_token = request.headers.get("Authorization", "")
        response = self.check_for_acc(data, auth_token)

        if response == 500:
            res = (
                {"message": ACCOUNT_SERVICE_DOWN},
                response,
            )
            log.info("response %s", res)
            return res

        log.info("response %s", response.json())

        if response.json()["is_present"]:
            message = ACCOUNT_EXISTS
            loan.save_to_db()
            return (
                {
                    "message": message,
                    "username": response.json()["username"],
                    "Approved Loan": loan.json(),
                },
                201,
            )
        else:
            return {"message": ACCOUNT_NOT_FOUND}, 401

    @classmethod
    def check_for_acc(cls, data, auth_token: str):
        try:
            url = ACCOUNT_SERVICE_IS_PRESENT_URL
            response = requests.post(
                url,
                data={"acc_id": data["acc_id"]},
                headers={"Authorization": auth_token},
            )
        except Exception:
            return 500
        return response
