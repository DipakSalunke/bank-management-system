from resources.security import token_required
from flask_restful import Resource, reqparse
import requests
from datetime import datetime
from models.loan import LoanModel
from json import dumps
from flask import request

import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s '+__name__+' %(threadName)s : %(message)s')
log = logging.getLogger()


class Loan(Resource): 
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
        
        log.debug("acc_id: %s", data["acc_id"])
        
        loans = LoanModel.find_by_accid(data["acc_id"])
        loans = [loan.json() for loan in loans]
        
        log.debug("loans %s",loans)
        
        if len(loans) > 0:
            return {"loans": loans}, 200
        else:
            return {'message': 'Loans not found for given account'}, 404

    @token_required
    def post(self):
        data = Loan.parser.parse_args()
        loan = LoanModel(str(datetime.utcnow()), **data)
        auth_token = request.headers.get('Authorization', '')
        response = self.check_for_acc(data, auth_token)
        
        log.info("response %s",response.json())
        
        if response.status_code == 500:
            return response
        if response.json()["is_present"]:
            message = "Account exists loan acceppted"
            loan.save_to_db()
            return {"message": message, "username": response.json()["username"], "Approved Loan": loan.json()}, 201
        else:
            return {"message": "You need account to get a loan, register first!"}, 401

    def check_for_acc(self, data, auth_token):
        try:
            url = 'http://127.0.0.1:5002/account/ispresent'
            response = requests.post(url, data={"acc_id": data["acc_id"]}, headers={
                                     'Authorization': auth_token})
        except Exception:
            return "Account service is not working try after some time", 500
        return response
