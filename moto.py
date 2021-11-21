#!/usr/bin/env python
import argparse
from datetime import datetime
import hashlib
import json
import hmac
import time

from bs4 import BeautifulSoup
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HNAP_URI = "https://192.168.100.1/HNAP1/"
SOAP_NAMESPACE = "http://purenetworks.com/HNAP1/"

KNOWN_ACTIONS = [
    "GetHomeConnection",
    "GetHomeAddress",
    "GetMotoStatusSoftware",
    "GetMotoStatusLog",
    "GetMotoLagStatus",
    "GetMotoStatusConnectionInfo",
    "GetMotoStatusDownstreamChannelInfo",
    "GetMotoStatusStartupSequence",
    "GetMotoStatusUpstreamChannelInfo",
]

session = requests.Session()
session.verify = False


def millis():
    return int(round(time.time() * 1000)) % 2000000000000


def md5sum(key, data):
    h = hmac.new(key.encode("utf-8"), digestmod=hashlib.md5)
    h.update(data.encode("utf-8"))
    return h.hexdigest()


def hnap_auth(key, data):
    return md5sum(key, data).upper() + " " + str(millis())


def do_action(action, params):
    action_uri = f'"{SOAP_NAMESPACE}{action}"'
    private_key = session.cookies.get("PrivateKey", path="/", default="withoutloginkey")

    response = session.post(
        HNAP_URI,
        data=json.dumps({action: params}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "SOAPAction": action_uri,
            "HNAP_AUTH": hnap_auth(private_key, str(millis()) + action_uri),
        },
    )

    try:
        response = json.loads(response.content.strip())
    except json.JSONDecodeError:
        print(response.content)
        raise

    return response[action + "Response"]


def do_actions(*actions):
    return do_action("GetMultipleHNAPs", {action: "" for action in actions})


def login(username, password):
    response = do_action(
        "Login",
        {
            "Action": "request",
            "Captcha": "",
            "LoginPassword": "",
            "PrivateLogin": "LoginPassword",
            "Username": username,
        },
    )

    private_key = md5sum(
        response["PublicKey"] + password, response["Challenge"]
    ).upper()

    session.cookies.set("uid", response["Cookie"], path="/")
    session.cookies.set("PrivateKey", private_key, path="/")

    response = do_action(
        "Login",
        {
            "Action": "login",
            "Captcha": "",
            "LoginPassword": md5sum(private_key, response["Challenge"]).upper(),
            "PrivateLogin": "LoginPassword",
            "Username": username,
        },
    )

    return response


def main():
    login("admin", "fuckyou")

    results = do_actions(*KNOWN_ACTIONS)

    print(json.dumps({"ts": datetime.now().isoformat(), "data": results}))


if __name__ == "__main__":
    main()
