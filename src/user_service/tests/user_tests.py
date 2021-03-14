import pytest
from db import db
from app import app
import json

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datatest.db"
app.config["JWT_SECRET_KEY"] = "superrr-secret"
db.init_app(app)
tester = app.test_client()
headers = {"Content-type": "application/json"}
headers_ref = {"Content-type": "application/json"}

user = json.dumps({"username": "jen", "password": "jen12"})
user2 = json.dumps({"username": "dipak", "password": "dipak12"})


token_start = "Bearer {}"


class TestUserRegister:
    url = "user/register"

    def test_post(self):
        res = tester.post(self.url, data=user, headers=headers)
        assert res.status_code == 201

    def test_post_dup(self):
        res = tester.post(self.url, data=user, headers=headers)
        assert res.status_code == 400

    def test_post_check(self):
        res = tester.post(self.url, data=user2, headers=headers)
        assert res.status_code == 201


class TestUserLogin:
    url = "/user/login"

    def test_auth_success(self):

        response = tester.post(
            self.url,
            json={"username": "dipak", "password": "dipak12"},
            headers=headers,
        )
        status = response.status_code
        assert status == 200

        headers["Authorization"] = token_start.format(response.json["access_token"])
        headers_ref["Authorization"] = token_start.format(
            response.json["refresh_token"]
        )

    def test_auth_failed(self):
        response = tester.post(
            self.url,
            json={"username": "dipakk", "password": "dipak412"},
            headers=headers,
        )
        status = response.status_code
        assert status == 401


class TestUsercheck:
    def test_user_present(self):
        response = tester.post(
            "/user/ispresent", json={"username": "dipak"}, headers=headers
        )
        status = response.status_code
        assert status == 200

    def test_user_not_present(self):
        response = tester.post(
            "/user/ispresent", json={"username": "dipakk"}, headers=headers
        )
        status = response.status_code
        assert status == 400


class TestUser:
    def test_get(self):
        response = tester.get("/user/1", headers=headers)
        status = response.status_code
        assert status == 200

    def test_not_found(self):
        response = tester.get("/user/13", headers=headers)
        status = response.status_code
        assert status == 404

    def test_delete_not_admin(self):
        response = tester.delete("/user/2", headers=headers)
        status = response.status_code
        assert status == 401

    def test_auth_for_admin(self):
        response = tester.post(
            "/user/login", json={"username": "jen", "password": "jen12"}
        )
        status = response.status_code
        assert status == 200
        global headers

        headers = {"Authorization": "Bearer {}".format(response.json["access_token"])}
        global headers_ref
        headers_ref = {
            "Authorization": token_start.format(response.json["refresh_token"])
        }

    def test_delete(self):
        response = tester.delete("/user/2", headers=headers)
        status = response.status_code
        assert status == 200

    def test_delete_not_found(self):
        response = tester.delete("/user/13", headers=headers)
        status = response.status_code
        assert status == 404

    def test_delete_admin(self):
        response = tester.delete("/user/1", headers=headers)
        status = response.status_code
        assert status == 400


class TestUserLogout:
    def test_logout(self):
        response = tester.post("/user/logout", headers=headers)
        status = response.status_code
        assert status == 200


class TestRefresh:
    def test_refresh(self):
        response = tester.post("/user/refresh", headers=headers_ref)
        status = response.status_code
        assert status == 200

        clear()


def clear():
    import os

    os.remove("./src/user_service/datatest.db")
