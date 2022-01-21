import app
import time
import pytest
import requests

# login endpoint tests
def test_login_request_with_valid_credentials():
    response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)

    assert response.status_code == 200
    assert len(response.json()["ticket"]) > 0


@pytest.mark.skip(reason="not testing this at the moment")
def test_login_request_ticket_expires_after_30_seconds():
    try:
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)

        assert response.status_code == 200
        response_body = response.json()
        ticket = response_body["ticket"]
        time.sleep(31)
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)
        response_body = response.json()
        assert ticket != response_body["ticket"]
    except Exception as ex:
        print(ex)


@pytest.mark.skip(reason="not testing this at the moment")
def test_login_request_ticket_doesn_not_expires_before_30_seconds():
    try:
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)

        assert response.status_code == 200
        response_body = response.json()
        ticket = response_body["ticket"]
        time.sleep(25)
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)
        response_body = response.json()
        assert ticket == response_body["ticket"]
    except Exception as ex:
        print(ex)


def test_login_request_with_null_token():
    try:
        response = app.send_login_request(" ", app._AUTH, app._PARAMS_LOGIN_OK)

        assert response.json()["ticket"] == None
    except Exception as ex:
        print(ex)


def test_login_request_with_null_auth():
    try:
        response = app.send_login_request(app._TOKEN, " ", app._PARAMS_LOGIN_OK)

        assert response.status_code == 403
        assert response.json()["errorType"] == "BadCredentialsException"
    except Exception as ex:
        print(ex)


def test_login_request_with_invalid_auth():
    try:
        response = app.send_login_request(
            app._TOKEN, app._INVALID_AUTH, app._PARAMS_LOGIN_OK
        )

        assert response.status_code == 403
        assert response.json()["errorMessage"] == "Forbidden Access to the resource"
    except Exception as ex:
        print(ex)


def test_login_request_with_invalid_application():
    try:
        response = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_BAD_GROUP
        )

        assert response.status_code == 400
        assert response.json()["error"] == "Bad Request"
    except Exception as ex:
        print(ex)


# encrypt endpoint tests
def test_encrypt_request_with_valid_data():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_content = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_content.status_code == 200
        assert len(response_content.json()["content"] > 0)
        assert response_content.json()["content"] != None
    except Exception as ex:
        print(ex)


def test_encrypt_request_with_invalid_data():
    try:
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)

        assert response.status_code == 200
        ticket = response.json()["ticket"]

        response_content = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            "spaces    ",
            "invalid",
            ticket,
        )

        assert response_content.status_code == 400
        assert response_content.json()["error"] == "Bad Request"
    except Exception as ex:
        print(ex)


def test_encrypt_request_with_no_auth():
    try:
        response = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            "spaces    ",
            "invalid",
            "no ticket",
        )

        assert response.status_code == 400
        assert response.json()["error"] == "Bad Request"
    except Exception as ex:
        print(ex)


def test_encrypt_request_with_null_token():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            " ",
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        assert response_encrypt.json()["content"] == None
    except Exception as ex:
        print(ex)


def test_encrypt_request_with_invalid_application():
    try:
        response = app.send_login_request(app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK)

        assert response.status_code == 200
        ticket = response.json()["ticket"]

        response_content = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_BAD_GROUP,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )
        assert response_content.json()["content"] == None
    except Exception as ex:
        print(ex)


# decrypt endopont tests
def test_decrypt_request_with_valid_data():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        content = response_encrypt.json()["content"]

        response_decrypt = app.send_decrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            content,
            ticket,
        )

        assert response_decrypt.json()["content"] == app._CONTENT
    except Exception as ex:
        print(ex)


def test_decrypt_request_with_invalid_content():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200

        response_decrypt = app.send_decrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            "invalid content",
            ticket,
        )

        assert response_decrypt.status_code == 200
        assert response_decrypt.json()["content"] == None
    except Exception as ex:
        print(ex)


def test_decrypt_request_with_invalid_intent():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        content = response_encrypt.json()["content"]

        response_decrypt = app.send_decrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK_INSTANCE2,
            content,
            ticket,
        )

        assert response_decrypt.status_code == 200
        assert response_decrypt.json()["content"] == None
    except Exception as ex:
        print(ex)


def test_decrypt_request_with_no_auth():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        content = response_encrypt.json()["content"]

        response_decrypt = app.send_decrypt_request(
            app._TOKEN,
            " ",
            app._PARAMS_LOGIN_BAD_GROUP,
            content,
            ticket,
        )

        assert response_decrypt.status_code == 403
        assert response_decrypt.json()["errorType"] == "BadCredentialsException"

    except Exception as ex:
        print(ex)


def test_decrypt_request_with_null_token():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["WRITE"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        content = response_encrypt.json()["content"]

        response_decrypt = app.send_decrypt_request(
            " ",
            app._AUTH,
            app._PARAMS_LOGIN_BAD_GROUP,
            content,
            ticket,
        )

        assert response_decrypt.status_code == 200
        assert response_decrypt.json()["content"] == None
    except Exception as ex:
        print(ex)


def test_decrypt_request_with_intent_READ():
    try:
        response_login = app.send_login_request(
            app._TOKEN, app._AUTH, app._PARAMS_LOGIN_OK
        )

        assert response_login.status_code == 200
        ticket = response_login.json()["ticket"]

        response_encrypt = app.send_encrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK,
            app._CONTENT,
            app._INTENT["READ"],
            ticket,
        )

        assert response_encrypt.status_code == 200
        content = response_encrypt.json()["content"]

        response_decrypt = app.send_decrypt_request(
            app._TOKEN,
            app._AUTH,
            app._PARAMS_LOGIN_OK_INSTANCE2,
            content,
            ticket,
        )

        assert (
            response_decrypt.json()["content"] == app._CONTENT
        ), "Decrypt of content failed"
    except Exception as ex:
        print(ex)
