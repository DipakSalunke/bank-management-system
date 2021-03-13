from flask import Flask, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from db import db
from ma import ma
from resources.loan import Loan

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loan.db"
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


api.add_resource(Loan, "/loan")

if __name__ == "__main__":
    app.run(port=5003, debug=True)
