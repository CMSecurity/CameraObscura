# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""

from jsonpickle import decode, encode
from flask import Flask, request, abort, send_file, make_response, send_from_directory, render_template
from werkzeug.utils import secure_filename
from core import config, logging, auth, util, actions
from core.actions import *
from datetime import datetime
from urllib import parse
from os.path import join, isfile
import hashlib
import re
app = Flask(__name__, template_folder=join(config.ROOT, 'templates'))
app.config["UPLOAD_FOLDER"] = "./dl/"
app.config["CACHE_TYPE"] = "null"
app.url_map.strict_slashes = False
ROUTES = None
ROOT = ""
LASTROUTE = None


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
    if route is not None:
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


@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def handleRoute(path):
    global ROUTES
    global LASTROUTE
    get = encode(request.args, unpicklable=False)
    post = encode(request.form, unpicklable=False)
    target = path
    if target == "":
        target = "/"

    logMessage = "{0} Request => Target {1}, GET {2}, POST {3}".format(
        request.method, target, get, post)
    logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), logMessage,
                "http", False, request.remote_addr, 0.0, sessionId(request))

    selectedRoute = None
    selectedPath = None
    for value in ROUTES:
        needle = path + getString(request)
        if len(path) > 0 and path[0] != "." and value != "" and re.match(
                value, needle):
            selectedRoute = ROUTES[value]
            selectedPath = value
            break

    if selectedRoute is None and path == "":
        selectedRoute = ROUTES[""]
        selectedPath = ""

    if selectedRoute is not None:
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), "{0} Request, Client {1}".format(
            request.method, request.headers.get('User-Agent')), "http", False, request.remote_addr, 0.0, sessionId(request))
        route = selectedRoute
        LASTROUTE = route
        for action in route["actions"]:
            result = actions.run(action, app, selectedPath,
                                 route, request, sessionId(request))
            if isinstance(result, bool) and result == False:
                abort(403)
            elif result is not None and isinstance(result, bool) == False:
                return result
    else:
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), "{0} Request, Client {1}, Result 404".format(
            request.method, request.headers.get('User-Agent')), "http", True, request.remote_addr, 0.0, None)
        abort(404)


def getString(request: request) -> str:
    result = ""
    get = request.query_string.decode("utf-8")
    if get == "":
        return result
    else:
        return "?" + get


def sessionId(request) -> str:
    userAgent = str(request.headers.get('User-Agent'))
    addr = request.remote_addr
    raw = userAgent + addr
    return hashlib.sha224(raw.encode('utf-8')).hexdigest()


def serve(path: str):
    global ROUTES
    global ROOT
    ROOT = path
    template = config.getConfigurationValue("http", "template")
    if template is None:
        raise Exception("No template is configured")
    routesFiles = join(config.ROOT, "templates", template, "routes.json")
    if isfile(routesFiles) == False:
        raise FileNotFoundError("Routes configuration was not found")
    ROUTES = parseRoutes(routesFiles)
    app.run(
        debug=config.getConfigurationValue("honeypot", "debug"),
        host=config.getConfigurationValue("http", "host"),
        port=int(config.getConfigurationValue("http", "port"))
    )
