from security import token_required
from flask_restful import Resource
import requests
from datetime import datetime
from models.loan import LoanModel
from flask import request
from schemas.loan import LoanSchema, AccountCheckSchema
import logging
from marshmallow import ValidationError
import json

logging.basicConfig(
    filename="./src/loan_service/loan.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s "
    + __name__
    + " %(threadName)s : %(message)s",
)
log = logging.getLogger("loan_log")

LOAN_NOT_FOUND = "Loans not found for given account"
ACCOUNT_SERVICE_DOWN = "Account service is not working try after some time"
ACCOUNT_EXISTS = "Account exists loan acceppted"
ACCOUNT_NOT_FOUND = "You need account to get a loan, register first!"
ACCOUNT_SERVICE_IS_PRESENT_URL = "http://127.0.0.1:5002/account/ispresent"

loan_schema = LoanSchema()
accountcheck_schema = AccountCheckSchema()


class Loan(Resource):
    @classmethod
    @token_required
    def get(cls):

        acc_id = accountcheck_schema.load(request.get_json())

        log.debug("acc_id: %s", acc_id)

        loans = LoanModel.find_by_accid(acc_id["acc_id"])
        loans = [loan_schema.dump(loan) for loan in loans]

        log.debug("loans %s", loans)

        if len(loans) > 0:
            return {"loans": loans}, 200
        else:
            return {"message": LOAN_NOT_FOUND}, 404

    @token_required
    def post(self):
        loan = loan_schema.load(request.get_json())
        loan.date = str(datetime.utcnow())
        auth_token = request.headers.get("Authorization", "")
        response = self.check_for_acc(loan.acc_id, auth_token)

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
                    "Approved Loan": loan_schema.dump(loan),
                },
                201,
            )
        else:
            return {"message": ACCOUNT_NOT_FOUND}, 401

    @classmethod
    def check_for_acc(cls, acc_id, auth_token: str):
        try:
            url = ACCOUNT_SERVICE_IS_PRESENT_URL
            response = requests.post(
                url,
                data=json.dumps({"acc_id": acc_id}),
                headers={
                    "Authorization": auth_token,
                    "Content-type": "application/json",
                },
            )
        except Exception:
            return 500
        return response
