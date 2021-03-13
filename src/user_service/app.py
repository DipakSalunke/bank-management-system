from flask import Flask, jsonify
from flask_restful import Api
from datetime import timedelta
import os
from db import db
from ma import ma
from security import jwt
from marshmallow import ValidationError
from resources.user import (
    UserRegister,
    UserCheck,
    User,
    UserLogin,
    TokenRefresh,
    UserLogout,
)

ACCESS_EXPIRES = timedelta(hours=1)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
# allow blacklisting for access and refresh tokens
app.config["JWT_SECRET_KEY"] = "super-secret"
# could do app.secret_key if we prefer
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

api = Api(app)
db.init_app(app)
ma.init_app(app)
# run before the first request to this instance of the application.


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt.init_app(app)

# Adds a resource to the api.

api.add_resource(UserRegister, "/user/register")
api.add_resource(UserCheck, "/user/ispresent")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/user/login")
api.add_resource(TokenRefresh, "/user/refresh")
api.add_resource(UserLogout, "/user/logout")

if __name__ == "__main__":
    app.run(port=5001, debug=True)
