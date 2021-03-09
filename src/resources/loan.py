from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from datetime import datetime
from models.loan import LoanModel
from json import dumps
class Loan(Resource):
    
    parser = reqparse.RequestParser()
    
    parser.add_argument('acc_id', required=True, type=str, help='account id cannot be blank')
    parser.add_argument('loan_type', required=True, type=str, help='loan type cannot be blank')
    parser.add_argument('loan_amt', required=True, type=float, help='loan ammount cannot be blank')
    parser.add_argument('rate_of_int', required=True, type=float, help='rate of interest cannot be blank')
    parser.add_argument('duration', required=True, type=float, help='duration cannot be blank')
  
    
    @jwt_required()
    def get(self):
        parser1 = reqparse.RequestParser()
        parser1.add_argument('acc_id', required=True, type=int, help='account id cannot be blank')
        data = parser1.parse_args()
        loans = LoanModel.find_by_accid(data["acc_id"])
        if loans:
            return {"loans": [loan.json() for loan in loans]},200 
        return {'message':'Loans not found for given account'},404
    
    @jwt_required()
    def post(self):
        data = Loan.parser.parse_args()
        loan = LoanModel(str(datetime.utcnow()) ,**data)
        loan.save_to_db()
        return loan.json(),201