from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from dotenv import load_dotenv
from db import db
from resources.account import Account, AccountCheck
from ma import ma

app = Flask(__name__)
load_dotenv(verbose = True)
app.config.from_object("dev_config")
app.config.from_envvar("APPLICATION_SETTINGS")

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
