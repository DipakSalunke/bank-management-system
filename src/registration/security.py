from flask_jwt_extended import JWTManager

from flask import Flask, jsonify

from blacklist import BLACKLIST
# used to add additional claims when creating a JWT.
jwt = JWTManager()

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
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({'description': 'the token is not fresh.',
                    'error': 'fresh_token_required'}), 401
# when a revoked token is encountered.


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'description': 'the token has been revoked',
                    'error': 'token_revoked'}), 401