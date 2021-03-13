from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from db import db
from resources.account import Account, AccountCheck
from ma import ma

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///account.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)
db.init_app(app)
ma.init_app(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Account, "/account")
api.add_resource(AccountCheck, "/account/ispresent")

if __name__ == "__main__":

    app.run(port=5002, debug=True)
