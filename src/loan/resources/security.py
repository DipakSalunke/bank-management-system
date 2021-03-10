from functools import wraps
from flask import request
import requests
def token_required(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        # Make endpoint in the Auth Service to validate an Auth Token
        auth_token = request.headers.get('Authorization', '')
        try:
            response = requests.get('http://127.0.0.1:5001/login', headers={'Authorization':auth_token})
            # If the Response status code is 200
        except Exception:
            return {"message":"server down try after some time"},500
        if response.status_code == 200:
            return f(*args, **kwargs)
        else:
            # error message
            return response.json()
    return wrapper_function