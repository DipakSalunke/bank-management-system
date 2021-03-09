import pytest
from app import app
import requests
tester = app.test_client()
headers = ''
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
    "acc_type": "Current"
}
account2 = {"username": "jenner", }
account.update(account)
account3 = {"username": "jenn", }
account3.update(account)
account4 = {"contact": "43636346", }
account4.update(account)



class TestUserLogin:
    def test_auth_success(self):
        response = requests.post(
            'http://127.0.0.1:5001/login', json={"username": "dipak", "password": "dipak12"})
        status = response.status_code
        print(response.json)
        assert status == 200
        global headers
        headers = {'Authorization': 'Bearer {}'.format(
            response.json()["access_token"])}


class TestAccount:
    url = '/account'
    def test_create_account(self):
        response = tester.put(self.url, data=account, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 201

    def test_create_account_not_a_user(self):
        response = tester.put(self.url, data=account2, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 400

    def test_create_account_is_a_user(self):
        response = tester.put(self.url, data=account3, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 201

    def test_update_account(self):
        response = tester.put(self.url, data=account4, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 201

    def test_get_account(self):
        response = tester.get(
            self.url, data={"username": "dipak"}, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 200


class TestAccountCheck:
    def test_check_account(self):
        response = tester.post('/account/ispresent',
                               data={"acc_id": 1}, headers=headers)
        status = response.status_code
        print(response.json)
        assert status == 200
