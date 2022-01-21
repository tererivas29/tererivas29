from types import resolve_bases
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import os
import logging

# logging.basicConfig(level=logging.DEBUG)

_BASE_URL = os.environ.get("API_URL")
_TOKEN = os.environ.get("TOKEN")
_AUTH = os.environ.get("AUTH")
_INVALID_AUTH = "randomcharacters"
_CONTENT = "test my app"

_PARAMS_LOGIN_OK = {
    "Id": "base64GUI",
    "name": "base64GUI2",
    "description": "myapp",
}

_PARAMS_LOGIN_OK_INSTANCE2 = {
    "Id": "base64GUI",
    "name": "base64GUI2",
    "description": "myapp2",
}

_PARAMS_LOGIN_BAD_GROUP = {
    "Id": "not 64",
    "name": "base64GUI2",
    "description": "myapp",
}

_INTENT = {"READ": "001", "WRITE": "002"}
DEFAULT_TIMEOUT = 2  # seconds


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def send_request(request, url, command, token, auth):
    # define a retry strategy
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],
        allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST"],
    )

    session = requests.Session()

    # set up retries and timeouts
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    session.mount("http://", TimeoutHTTPAdapter(max_retries=retries))
    return session.post(
        f"{url}/{command}/{token}",
        data=json.dumps(request),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
            "Cache-Control": "no-cache",
        },
    )


def send_login_request(token, auth, params):

    return send_request(params, _BASE_URL, "login", token, auth)


def send_encrypt_request(token, auth, login_params, content, intent, ticket):
    request = {
        "application": login_params,
        "content": content,
        "intent": intent,
        "ticket": ticket,
    }

    # print(f"=========request {request}")

    return send_request(request, _BASE_URL, "encrypt", token, auth)


def send_decrypt_request(token, auth, login_params, content, ticket):
    request = {
        "application": login_params,
        "content": content,
        "ticket": ticket,
    }

    return send_request(request, _BASE_URL, "decrypt", token, auth)
