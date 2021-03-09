from functools import wraps
from flask import request
import requests
def token_required(f):
    @wraps(f)
    def wrapper_function(*args, **kwargs):
        # Make endpoint in the Auth Service to validate an Auth Token
        auth_token = request.headers.get('Authorization', '')
        response = requests.get('http://127.0.0.1:5001/login', headers={'Authorization':auth_token})
        # If the Response status code is 200
        if response.status_code == 200:
            return f(*args, **kwargs)
        else:
            # error message
            return response.json(),401
    return wrapper_function