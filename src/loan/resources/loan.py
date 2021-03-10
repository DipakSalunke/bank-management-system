from resources.security import token_required
from flask_restful import Resource, reqparse
import requests
from datetime import datetime
from models.loan import LoanModel
from json import dumps
from flask import request

class Loan(Resource):
    #method_decorators = {'get': [token_required]}
    parser = reqparse.RequestParser()

    parser.add_argument('acc_id', required=True, type=str,
                        help='account id cannot be blank')
    parser.add_argument('loan_type', required=True, type=str,
                        help='loan type cannot be blank')
    parser.add_argument('loan_amt', required=True, type=float,
                        help='loan ammount cannot be blank')
    parser.add_argument('rate_of_int', required=True,
                        type=float, help='rate of interest cannot be blank')
    parser.add_argument('duration', required=True,
                        type=float, help='duration cannot be blank')

    @token_required
    def get(self):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('acc_id', required=True,
                             type=int, help='account id cannot be blank')
        data = parser1.parse_args()
        loans = LoanModel.find_by_accid(data["acc_id"])
        if loans:
            return {"loans": [loan.json() for loan in loans]}, 200
        return {'message': 'Loans not found for given account'}, 404

    @token_required
    def post(self):
        data = Loan.parser.parse_args()
        loan = LoanModel(str(datetime.utcnow()), **data)
        auth_token = request.headers.get('Authorization', '')
        response = self.check_for_acc(data, auth_token)
        if 500 in response:
            return response
        print(response.json())
        if response =="True":
            message = "Account exists loan acceppted"
            loan.save_to_db()
            return {"message": message, "username": response.json()["username"], "Approved Loan": loan.json()}, 201
        else:
            return {"message": "You need account to get a loan, register first!"},401
        

    def check_for_acc(self, data, auth_token):
        try:
            url = 'http://127.0.0.1:5002/account/ispresent'
            response = requests.post(url, data={"acc_id": data["acc_id"]},headers={'Authorization':auth_token})
        except Exception:
            response =  "Account service is not working try after some time",500
        return response
