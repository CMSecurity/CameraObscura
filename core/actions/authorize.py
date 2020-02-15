# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Receives the username and password from a login request
"""
from datetime import datetime
import urllib
from flask import Flask, request
from core import logging


def run(app: Flask, selectedPath: str, route: object,
        request: request):
    if "authorize" not in route:
      raise Exception("Authorize action options missing")
    
    username = route["authorize"]["username"]
    password = route["authorize"]["password"]

    get = request.args
    query_string = request.query_string.decode("utf-8")
    # if the query_string is an %-encoded query string (contains %3) -> Reparse the string to get the dictionary
    # Flask seems not to unquote them and puts the complete query string as a key into the request.args dictionary, which is hard to log
    if "%3" in query_string:
        unquoted = urllib.parse.unquote(query_string)
        get_params = urllib.parse.parse_qs(unquoted)
        get = get_params
    post = request.form

    credentials = {
      "username": None,
      "password": None
    }

    haystacks = [
      get,
      post
    ]
    username_existing = False
    password_existing = False

    for haystack in haystacks:
      for key, value in haystack.items():
        if key == username:
          username_existing = True
        if key == password:
          password_existing = True
        if key == username or key == password:
          credentials_key = "username" if key == username else "password"
          if isinstance(value, list) and len(value) > 0:
            credentials[credentials_key] = value[0]
          else:
            credentials[credentials_key] = value

    
    if username_existing and password_existing:
      logging.log(logging.EVENT_ID_LOGIN,
                  datetime.now(),
                  "Login attempt [{0}/{1}] succeeded".format(credentials["username"], credentials["password"]),
                  False,
                  request.remote_addr,
                  username=credentials["username"], password=credentials["password"])

