from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.account import Account
from resources.loan import Loan

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'dipak'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister,"/register")
api.add_resource(Account,"/account")
api.add_resource(Loan,"/loan")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)