import pytest
from requests import Response
from functools import wraps
from mock import patch
from werkzeug.datastructures import Headers
from db import db


def decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)

    return decorated_function


patch("security.token_required", decorator).start()

the_response = Response()
the_response.status_code = 400


check = patch("resources.loan.Loan.check_for_acc", return_value=the_response)

from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datatest.db"
db.init_app(app)

tester = app.test_client()

loan_details = {
    "acc_id": "1",
    "loan_type": "education",
    "loan_amt": 34323.5,
    "rate_of_int": 12.3,
    "duration": 4.5,
}


class TestLoan:
    url = "/loan"

    def test_create_loan(self):
        the_response._content = b'{"is_present":true,"username":"test"}'
        check.start()
        response = tester.post(self.url, data=loan_details)
        status = response.status_code
        assert status == 201

    def test_create_loan_not_a_user(self):
        the_response._content = b'{"is_present":false}'
        check.start()
        response = tester.post(self.url, data=loan_details)
        status = response.status_code
        assert status == 401

    def test_get_loan(self):
        response = tester.get(self.url, data={"acc_id": "1"})
        status = response.status_code
        assert status == 200

    def test_get_loan_acc_unavailable(self):
        response = tester.get(self.url, data={"acc_id": "13"})
        status = response.status_code
        assert status == 404
        clear()


def clear():
    import os

    os.remove("./src/loan_service/datatest.db")
