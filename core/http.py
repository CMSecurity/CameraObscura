# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""


from datetime import datetime
from os.path import join, isfile
import re
import hashlib
from jsonpickle import decode, encode
from flask import Flask, request, abort, render_template
from core import config, logging, util, actions
from core.actions import *
app = Flask(__name__, template_folder=join(config.ROOT, 'templates'))
app.config["UPLOAD_FOLDER"] = "./dl/"
app.config["CACHE_TYPE"] = "null"
app.url_map.strict_slashes = False
ROUTES = None
ROOT = ""
LASTROUTE = None


def parseRoutes(file: str) -> object:
    """
    parses the JSON routes file.
    """
    content = ""
    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError as e:
        print(e)

    obj = decode(content)
    return obj


@app.after_request
def add_header(response):
    """
    Adds a header if the configured routes has some
    """
    route = LASTROUTE
    if route is not None:
        if "headers" in route:
            for key, value in route["headers"].items():
                response.headers[key] = value
    return response


@app.errorhandler(404)
def page_not_found(e):
    """
    Render the 404 error
    """
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    """
    Render the 403 error
    """
    return render_template('403.html'), 403


@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def handleRoute(path):
    """
    Tries to execute a given route based on the path
    """
    global ROUTES
    global LASTROUTE
    get = request.args
    post = request.form
    userAgent = request.headers.get('User-Agent')
    target = path
    if target == "":
        target = "/"

    logMessage = "{0} {1}".format(
        request.method, target, get, post, userAgent)

    selectedRoute = None
    selectedPath = None
    for value in ROUTES:
        needle = path + getString(request)
        if path and path[0] != "." and value != "" and re.match(
                value, needle):
            selectedRoute = ROUTES[value]
            selectedPath = value
            break

    if selectedRoute is None and path == "":
        selectedRoute = ROUTES[""]
        selectedPath = ""

    if selectedRoute is not None:
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), logMessage, False, request.remote_addr,useragent=userAgent, get=get, post=post)
        route = selectedRoute
        LASTROUTE = route
        for action in route["actions"]:
            result = actions.run(action, app, selectedPath,
                                 route, request)
            if isinstance(result, bool) and result is False:
                abort(403)
            elif result is not None and isinstance(result, bool) is False:
                return result
    else:
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), logMessage, True, request.remote_addr)
        abort(404)


def getString(requestObj) -> str:
    """
    Returns the HTTP GET string out of the given request
    """
    result = ""
    get = requestObj.query_string.decode("utf-8")
    if get == "":
        return result
    return "?" + get


def serve(path: str):
    """
    Start the server
    @param path is the base path of the software
    """
    global ROUTES
    global ROOT
    ROOT = path
    template = config.getConfigurationValue("http", "template")
    if template is None:
        raise Exception("No template is configured")
    routesFiles = join(config.ROOT, "templates", template, "routes.json")
    if isfile(routesFiles) is False:
        raise FileNotFoundError("Routes configuration was not found")
    ROUTES = parseRoutes(routesFiles)
    app.run(
        debug=config.getConfigurationValue("honeypot", "debug"),
        host=config.getConfigurationValue("http", "host"),
        port=int(config.getConfigurationValue("http", "port"))
    )
