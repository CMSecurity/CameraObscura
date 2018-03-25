# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Does an authorization via HTTP GET or POST.
"""
from datetime import datetime
import re
from core import logging, auth, config

def run(app, selectedPath: str, route: object,
        requestObj, sessionId: str):
    """
    Executes the authorize action
    """
    return authorize(route, requestObj, sessionId)


def authorize(route: object, requestObj, sessionId: str) -> bool:
    """
    Tries to authorize a user based on a requestObj
    """
    # extract credentials
    user, password = tryToFindPassword(requestObj.args)
    if requestObj.method == "POST" and (user == "" or password == ""):
        user, password = tryToFindPassword(requestObj.form)

    # Verify with user db
    authResult = auth.isAuthorized(user, password)
    message = ""
    if authResult:
        message = "Login attempt [{0}/{1}] succeeded".format(user, password)
    else:
        message = "Login attempt [{0}/{1}] failed".format(user, password)
    logging.log(
        logging.EVENT_ID_LOGIN,
        datetime.now(),
        message,
        "http",
        authResult,
        requestObj.remote_addr,
        0.0,
        sessionId)
    return authResult


def tryToFindPassword(haystack: dict) -> (str, str):
    """
    Tries to harvest credentials, e. g. out of HTTP GET
    """
    userNameRegex = config.getConfigurationValue("http", "usernameregex")
    passwordRegex = config.getConfigurationValue("http", "passwordregex")
    userName = ""
    password = ""
    for key in haystack:
        value = haystack.get(key)
        if userName == "" and re.match(userNameRegex, key) is not None:
            userName = value
        if password == "" and re.match(passwordRegex, key) is not None:
            password = value

        if password != "" and userName != "":
            break

    return (userName, password)
