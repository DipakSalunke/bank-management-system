import pytest
from requests import Response
from functools import wraps
from mock import patch
from db import db
import json


def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


patch("security.token_required", decorator).start()

the_response = Response()
the_response.status_code = 400
the_response._content = b'{"is_present": false}'

patch("resources.account.Account.check_for_user", return_value=the_response).start()
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datatest.db"
db.init_app(app)

tester = app.test_client()

headers = {"Content-type": "application/json"}
account = {
    "username": "dipak",
    "name": "dipak salunke",
    "address": "pune",
    "state": "MH",
    "country": "India",
    "email": "abc@gmail.com",
    "pan": "ACGDE123",
    "contact": "123456789",
    "dob": "11-11-10",
    "acc_type": "Current",
}
account2 = {
    "username": "jenner",
}
account.update(account)
account3 = {
    "username": "jenn",
}
account3.update(account)
account4 = {
    "contact": "43636346",
}
account4.update(account)

account = json.dumps(account)
account2 = json.dumps(account2)
account3 = json.dumps(account3)
account4 = json.dumps(account4)


class TestAccount:
    url = "/account"

    def test_create_account(self):
        response = tester.put(self.url, data=account, headers=headers)
        status = response.status_code
        assert status == 201

    def test_create_account_not_a_user(self):
        response = tester.put(self.url, data=account2, headers=headers)
        status = response.status_code
        assert status == 400

    the_response._content = b'{"is_present": true}'
    patch("resources.account.Account.check_for_user", return_value=the_response).start()

    def test_create_account_is_a_user(self):
        response = tester.put(self.url, data=account3, headers=headers)
        status = response.status_code
        assert status == 201

    def test_update_account(self):
        response = tester.put(self.url, data=account4, headers=headers)
        status = response.status_code
        assert status == 201

    def test_get_account(self):
        response = tester.get(
            self.url, data=json.dumps({"username": "dipak"}), headers=headers
        )
        status = response.status_code
        assert status == 200


class TestAccountCheck:
    def test_check_account(self):
        response = tester.post(
            "/account/ispresent", data=json.dumps({"acc_id": 1}), headers=headers
        )
        status = response.status_code
        assert status == 200

        clear()


def clear():
    import os

    os.remove("./src/account_service/datatest.db")
