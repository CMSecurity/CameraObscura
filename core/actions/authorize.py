# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Does an authorization via HTTP GET or POST.
"""
from flask import Flask, request
from core import logging, auth, config
from datetime import datetime
import re
def run(app: Flask, route: object, request: request, sessionId: str):
  return authorize(route, request, sessionId)

def authorize(route: object, request: request, sessionId: str) -> bool:
  # extract credentials
  user, password = tryToFindPassword(request.args)
  if request.method == "POST" and (user == "" or password == ""):
    user, password = tryToFindPassword(request.form)

  # Verify with user db
  authResult=auth.isAuthorized(user, password)
  message = ""
  if authResult:
    message = "Login attempt [{0}/{1}] succeeded".format(user, password)
  else: 
    message = "Login attempt [{0}/{1}] succeeded".format(user, password) 
  logging.log(logging.EVENT_ID_LOGIN,datetime.now(),message,"http",False,request.remote_addr,0.0,sessionId)
  return authResult

def tryToFindPassword(haystack: dict) -> (str, str):
  userNameRegex=config.getConfigurationValue("http","usernameregex")
  passwordRegex=config.getConfigurationValue("http","passwordregex")
  userName=""
  password=""
  for key in haystack:
    value = haystack.get(key)
    if userName == "" and re.match(userNameRegex, key) != None:
      userName = value
    if password == "" and re.match(passwordRegex, key) != None:
      password = value  

    if password != "" and userName != "":
      break
  
  return (userName, password)