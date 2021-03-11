import pytest
from db import db
from app import app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///datatest.db"
db.init_app(app)
tester = app.test_client()
headers = ''
headers_ref = ''
cust = {
    "username": "dipak",
    "password": "dipak12",
    "name": "dipak",
    "address": "pune",
    "state": "MH",
    "country": "India",
    "email": "abc@gmail.com",
    "pan": "ACGD123",
    "contact": "123456789",
    "dob": "10-10-10",
    "acc_type": "Savings"
}

user = {
    "username": "jen",
    "password": "jen12"}
user2 = {
    "username": "jenn",
    "password": "jenn12"}


class TestCustRegister:
    def test_post_cust(self):
        res = tester.post('/register/customer', data=cust)
        assert res.status_code == 201

    def test_post_check(self):
        res = tester.post('/register/customer', data=cust)
        assert res.status_code == 400


class TestUserRegister:
    url = '/register/user'

    def test_post(self):
        res = tester.post(self.url, data=user)
        assert res.status_code == 201

    def test_post_dup(self):
        res = tester.post('/register/user', data=user)
        assert res.status_code == 400

    def test_post_check(self):
        res = tester.post(self.url, data=user2)
        assert res.status_code == 201


class TestUserLogin:
    def test_auth_success(self):
        response = tester.post(
            '/login', json={"username": "dipak", "password": "dipak12"})
        status = response.status_code
        assert status == 200
        global headers

        headers = {'Authorization': 'Bearer {}'.format(
            response.json["access_token"])}
        global headers_ref
        headers_ref = {'Authorization': 'Bearer {}'.format(
            response.json["refresh_token"])}

    def test_auth_failed(self):
        response = tester.post(
            '/login', json={"username": "dipakk", "password": "dipak412"})
        status = response.status_code
        assert status == 401


class TestUsercheck:
    def test_user_present(self):
        response = tester.post(
            '/user/ispresent', json={"username": "dipak"}, headers=headers)
        status = response.status_code
        assert status == 200

    def test_user_not_present(self):
        response = tester.post(
            '/user/ispresent', json={"username": "dipakk"}, headers=headers)
        status = response.status_code
        assert status == 400


class TestUser:
    def test_get(self):
        response = tester.get(
            '/user/1', headers=headers)
        status = response.status_code
        assert status == 200

    def test_not_found(self):
        response = tester.get(
            '/user/13', headers=headers)
        status = response.status_code
        assert status == 404

    def test_delete(self):
        response = tester.delete(
            '/user/2', headers=headers)
        status = response.status_code
        assert status == 200

    def test_delete_not_found(self):
        response = tester.delete(
            '/user/13', headers=headers)
        status = response.status_code
        assert status == 404

    def test_delete_admin(self):
        response = tester.delete(
            '/user/1', headers=headers)
        status = response.status_code
        assert status == 400


class TestUserLogout:
    def test_logout(self):
        response = tester.post(
            '/logout', headers=headers)
        status = response.status_code
        assert status == 200


class TestRefresh:
    def test_refresh(self):
        response = tester.post(
            '/refresh', headers=headers_ref)
        status = response.status_code
        assert status == 200

        clear()


def clear():
    import os
    os.remove("./src/registration/datatest.db")
