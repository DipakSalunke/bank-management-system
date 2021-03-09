from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from blacklist import BLACKLIST
from db import db
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
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
api = Api(app)
db.init_app(app)
# Registers a function to be run before the first request to this instance of the application.
 

@app.before_first_request
def create_tables():
    db.create_all()


# Create the JWTManager instance.
jwt = JWTManager(app)

# used to add additional claims when creating a JWT.


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


#used to check if a JWT has been revoked.
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    print(jwt_payload,jwt_header)
    return jwt_payload['jti'] in BLACKLIST

# when an expired JWT is encountered.
@jwt.expired_token_loader
def expire_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# when an invalid JWT is encountered.


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description': 'Signature verification falied.',
                    'error': 'invalid_token'}), 401

# when no JWT is present.


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'description': 'request does not contain an access token',
                    'error': 'authorization_required'}), 401
# when a valid and non-fresh token is used on an endpoint that is marked as fresh=True.


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({'description': 'the token is not fresh.',
                    'error': 'fresh_token_required'}), 401
# when a revoked token is encountered.


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'description': 'the token has been revoked',
                    'error': 'token_revoked'}), 401


# Adds a resource to the api.
api.add_resource(CustRegister, "/register/customer")
api.add_resource(UserRegister, "/register/user")
api.add_resource(UserCheck, "/user/ispresent")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout,"/logout")
if __name__ == '__main__':
    app.run(port=5001, debug=True)
    
