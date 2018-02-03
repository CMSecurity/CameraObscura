# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""

from jsonpickle import decode
from flask import Flask, request, abort, send_file, make_response
from core import config, logging
from datetime import datetime
import re
app = Flask(__name__)
ROUTES=None

def parseRoutes(file: str) -> object:
  content = ""
  try: 
    with open(file, 'r') as f:
      content = f.read()
  except (Exception):
    pass
  
  obj = decode(content)
  return obj

@app.route('/', defaults={'path': ''}, methods = ['POST', 'GET'])
@app.route('/<path:path>', methods = ['POST', 'GET'])
def handleRoute(path):
  global ROUTES
  if path in ROUTES:
    route = ROUTES[path]
    for action in route["actions"]:
      if action == "log":
        log(request.method, request.remote_addr)
      if action == "servefile":
        return servefile(route, request)
      if action == "text":
        return route["text"]["text"]
      if action == "authorize":
        if authorize(route, request) == False:
          abort(403)
  else:
    abort(404)
  return path

def log(method: str, src_ip: str):
  logging.log(logging.EVENT_ID_HTTP, datetime.now(), "HTTP-{0} Request".format(method), "http", False, src_ip,0.0, "")

def servefile(route: object, request: request):
  return send_file(route["servefile"]["file"], as_attachment=False)

def authorize(route: object, request: request):

  # extract credentials
  user, password = tryToFindPassword(request.args)
  if request.method == "POST":
    user, password = tryToFindPassword(request.form)

  # Verify with user db

  
  return False

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

def serve():
  global ROUTES
  ROUTES=parseRoutes("routes.json")
  app.run(
        debug=True
    )
 