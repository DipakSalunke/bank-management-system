from blacklist import BLACKLIST
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from libs.strings import gettext
# logger configuration
import logging

from schemas.user import UserSchema, UserCheckSchema
from marshmallow import ValidationError

logging.basicConfig(
    filename="./src/registration/registration.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s "
    + __name__
    + " %(threadName)s : %(message)s",
)
log = logging.getLogger("user_log")

user_schema = UserSchema()
usercheck_schema = UserCheckSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        """registers a new user in the system

        Returns:
            tuple: message and error code
        """
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": gettext("user_already_exists")}, 400
        user.save_to_db()
        log.info("user created:%s", user_schema.dump(user))
        return {"message": gettext("user_created")}, 201


class UserCheck(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """checks if username is present in the db

        Returns:
            tuple: message if present or not and return status code
        """
        user_data = usercheck_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data["username"])
        if user:
            log.info("user present:%s", user)
            return {"is_present": True}, 200
        else:
            log.info("user not present:%s", user_data)
            return {"is_present": False}, 400


class User(Resource):
    @classmethod
    @jwt_required(fresh=True)
    def get(cls, user_id: int):
        """get the user information of the given user id

        Args:
            user_id (int): user_id

        Returns:
            User: user details
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, user_id: int):
        """deletes user with provided user ID

        Args:
            user_id (int): users ID

        Returns:
            tuple: message nad status code
        """
        claims = get_jwt()
        print(claims)
        if not claims["is_admin"]:
            log.warning("delete user accessed by non admin")
            return {"message": gettext("user_admin_error")}, 401
        user = UserModel.find_by_id(user_id)

        if not user:
            log.info("user not found for id %s", user_id)
            return {"message": gettext("user_not_found")}, 404

        if user.id == 1:
            log.critical(
                "admin delete operation was requested %s", user_schema.dump(user)
            )
            return {"message": gettext("user_adm_delete")}, 400

        user.delete_from_db()
        log.warning("user deleted %s", user_schema.dump(user))
        return {"message": gettext("user_deleted")}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        """logs in user with valid username and password and password

        Returns:
            tuple: message and status code
        """
        user = user_schema.load(request.get_json())
        user_db = UserModel.find_by_username(user.username)
        # authenticate
        if user_db and safe_str_cmp(user_db.password, user.password):
            # identity
            access_token = create_access_token(identity=user_db.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            log.info(
                "user %s logged in ! tokens : access %s", user.username, access_token
            )
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"message": gettext("user_invalid_creds")}, 401

    @classmethod
    @jwt_required()
    def get(cls):
        """a authenticator for the jwt token sent for authentication by other services 
        """
        log.info("auth was requested by a service")


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        """logs the user out of the system by blacklisting the access token

        Returns:
            tuple : message and status code
        """
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        log.info("user with id %s logged out", get_jwt_identity())
        return {"message": gettext("user_logged_out").format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        """generates fresh token for the critical endpoint

        Returns:
            tuple: message and status code
        """
        current_user = get_jwt_identity()
        log.info("user with id %s requested refresh token ", get_jwt_identity())
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
