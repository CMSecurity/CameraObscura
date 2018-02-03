# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""

from jsonpickle import decode
from flask import Flask, request, abort, send_file, make_response
from core import config, logging, auth
from datetime import datetime
from random import randint
import pathlib
from PIL import Image, ImageDraw, ImageEnhance
from os import path
import re
app = Flask(__name__)
ROUTES=None
ROOT=""

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
  file = route["servefile"]["file"]
  
  if isinstance(file, list):
    fileToServe = file[randint(0, len(file) -1)]
  else:
    fileToServe = file
  

  if path.exists(path.abspath(fileToServe)):
    fileToServe=path.abspath(fileToServe)
  
  pathInfo = pathlib.Path(fileToServe)
  if "watermark" in route["servefile"] and route["servefile"]["watermark"] and pathInfo.suffix.replace(".","") in config.getConfigurationValue("image","images").replace(r"\s","").split(","):
    tmpPath = path.join(config.getConfigurationValue("image","workdir"), pathInfo.name + pathInfo.suffix)
    now = datetime.now().isoformat()
    original = Image.open(fileToServe)
    watermark = Image.new("RGBA", original.size)
    waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
    waterdraw.text((4, 2), "%s %s" % (config.getConfigurationValue("image","watermark"), now))
    original.paste(watermark, None, watermark)
    original.save(tmpPath)
    return send_file(tmpPath, as_attachment=False)

  return send_file(fileToServe, as_attachment=False)

def authorize(route: object, request: request) -> bool:

  # extract credentials
  user, password = tryToFindPassword(request.args)
  if request.method == "POST":
    user, password = tryToFindPassword(request.form)

  # Verify with user db
  return  auth.isAuthorized(user, password)

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

def serve(path: str):
  global ROUTES
  global ROOT
  ROOT = path
  ROUTES=parseRoutes("routes.json")
  app.run(
        debug=True,
        port=int(config.getConfigurationValue("http","port"))
    )
 