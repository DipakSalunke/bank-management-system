from functools import wraps
from flask import request
import requests
import logging

logging.basicConfig(
    filename="./src/account_service/account.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s "
    + __name__
    + " %(threadName)s : %(message)s",
)
log = logging.getLogger("security_log")


def token_required(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        # Make endpoint in the Auth Service to validate an Auth Token
        auth_token = request.headers.get("Authorization", "")
        try:
            response = requests.get(
                "http://127.0.0.1:5001/user/login",
                headers={"Authorization": auth_token},
            )
            log.info("authenticated successfully! %s", response)

        except Exception:
            log.critical("auth service is down")
            return {"message": "server is down ! try after some time"}, 500
        # If the Response status code is 200
        if response.status_code == 200:
            return f(*args, **kwargs)
        else:
            # error message
            log.warning("auth failed:%s", response.json())
            return response.json()

    return wrapper_function
