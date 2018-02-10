# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""

from jsonpickle import decode
from flask import Flask, request, abort, send_file, make_response, send_from_directory, render_template
from werkzeug.utils import secure_filename
from core import config, logging, auth, util
from datetime import datetime
import random
import pathlib
from PIL import Image, ImageDraw, ImageEnhance
from os import path, remove
from os.path import join
from shutil import move
from urllib import parse
import time
import hashlib
import re
app = Flask(__name__, template_folder=join(config.ROOT,'templates'))
app.config["UPLOAD_FOLDER"] = "./dl/"
app.config["CACHE_TYPE"] = "null"
app.url_map.strict_slashes = False
ROUTES=None
ROOT=""
LASTROUTE=None

def parseRoutes(file: str) -> object:
  content = ""
  try: 
    with open(file, 'r') as f:
      content = f.read()
  except (Exception):
    pass
  
  obj = decode(content)
  return obj


@app.after_request
def add_header(response):
  route = LASTROUTE
  if route != None:
    if "headers" in route:
      for key, value in route["headers"].items():
        response.headers[key] = value
  return response  


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403 

@app.route('/', defaults={'path': ''}, methods = ['POST', 'GET'])
@app.route('/<path:path>', methods = ['POST', 'GET'])
def handleRoute(path):
  global ROUTES
  global LASTROUTE
  if path in ROUTES:
    route = ROUTES[path]
    LASTROUTE = route
    for action in route["actions"]:
      if action == "sleep":
        time.sleep(float(route["sleep"]["duration"]))
      if action == "log":
        log(request.method, request.remote_addr,sessionId(request))
      if action == "catchfile":
        catchfile(route, request)
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

def log(method: str, src_ip: str, sessionId: str):
  logging.log(logging.EVENT_ID_HTTP, datetime.now(), "HTTP-{0} Request".format(method), "http", False, src_ip,0.0, sessionId)

def catchfile(route: object, request: request):
  if request.method == 'POST':
    for key in request.files:
      file = request.files.get(key)
      if file.filename != "":
          workdir= config.getConfigurationValue("honeypot","workdir")
          tmpFile = path.join(workdir, file.filename)  
          file.save(tmpFile)
          hash = util.getChecksum(tmpFile)
          dlPath = path.join(app.config['UPLOAD_FOLDER'], hash)
          if path.isfile(dlPath) == False:
            move(tmpFile, dlPath)
            logging.log(logging.EVENT_ID_UPLOAD, datetime.now(), "File {0} uploaded to dl/{1}".format(file.filename, hash), "http", False, request.remote_addr,0.0, sessionId(request))
          else:
            remove(tmpFile)
            logging.log(logging.EVENT_ID_UPLOAD, datetime.now(), "Not storing duplicate content {1}".format(file.filename, hash), "http", False, request.remote_addr,0.0, sessionId(request))



def servefile(route: object, request: request):
  file = route["servefile"]["file"]
  
  if isinstance(file, list):
    random.seed(datetime.now().time()) 
    fileToServe = join(config.ROOT,file[random.randint(0, len(file) -1)])
  else:
    fileToServe = join(config.ROOT,file)
  
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
  if "render_template" in route["servefile"] and route["servefile"]["render_template"] == True:
    getValues = getString(request)
    return render_template(route["servefile"]["file"], config=config, getValues=getValues)
  return send_file(fileToServe, as_attachment=False)

def getString(request) -> str:
  result=""
  for key in request.args:
    if result == "":
      result = result + "?"
    else:
       result = result + "&"
    result = result + parse.quote(key) + "=" + parse.quote(request.args.get(key))
  return result

def sessionId(request) -> str:
  userAgent = str(request.headers.get('User-Agent'))
  addr = request.remote_addr
  raw = userAgent + addr
  return hashlib.sha224(raw.encode('utf-8')).hexdigest()

def authorize(route: object, request: request) -> bool:

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
  logging.log(logging.EVENT_ID_LOGIN,datetime.now(),message,"http",False,request.remote_addr,0.0,sessionId(request))
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

def serve(path: str):
  global ROUTES
  global ROOT
  ROOT = path
  ROUTES=parseRoutes(join(config.ROOT,"routes.json"))
  app.run(
        debug=config.getConfigurationValue("honeypot","debug").lower() == 'true',
        host=config.getConfigurationValue("http","host"),
        port=int(config.getConfigurationValue("http","port"))
    )
