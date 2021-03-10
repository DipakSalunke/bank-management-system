from flask import Flask
from flask_restful import Api
from datetime import timedelta
from db import db
from security import jwt
from resources.user import (CustRegister,
                            UserRegister,
                            UserCheck, User,
                            UserLogin,
                            TokenRefresh,
                            UserLogout)

ACCESS_EXPIRES = timedelta(hours=1)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# flask jwt can raise its own exceptions and errors
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

api = Api(app)
db.init_app(app)

# run before the first request to this instance of the application.


@app.before_first_request
def create_tables():
    db.create_all()


jwt.init_app(app)

# Adds a resource to the api.

api.add_resource(CustRegister, "/register/customer")
api.add_resource(UserRegister, "/register/user")
api.add_resource(UserCheck, "/user/ispresent")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
