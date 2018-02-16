# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
""" 

from jsonpickle import decode
from flask import Flask, request, abort, send_file, make_response, send_from_directory, render_template
from werkzeug.utils import secure_filename
from core import config, logging, auth, util, actions
from core.actions import * 
from datetime import datetime
from urllib import parse
from os.path import join
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
      result=actions.run(action,app, route, request, sessionId(request))
      if isinstance(result, bool) and result == False:
        abort(403)
      elif result != None and isinstance(result, bool) == False:
        return result
  else:
    abort(404)
  return path

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

def serve(path: str):
  global ROUTES
  global ROOT
  ROOT = path
  ROUTES=parseRoutes(join(config.ROOT,"routes.json"))
  app.run(
        debug=config.getConfigurationValue("honeypot","debug"),
        host=config.getConfigurationValue("http","host"),
        port=int(config.getConfigurationValue("http","port"))
    )
