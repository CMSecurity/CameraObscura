# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module http related functionality
"""


from datetime import datetime
from os.path import join, isfile, isdir, isabs
import re
from jsonpickle import decode
from flask import Flask, request, abort, render_template
from core import config, logging, actions
from core.actions import *
from pathlib import Path
import urllib

app = Flask(__name__, template_folder=join(config.ROOT, 'templates'))
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
    query_string = request.query_string.decode("utf-8")

    # if the query_string is an %-encoded query string (contains %3) -> Reparse the string to get the dictionary
    # Flask seems not to unquote them and puts the complete query string as a key into the request.args dictionary, which is hard to log
    if "%3" in query_string:
        unquoted = urllib.parse.unquote(query_string)
        get = unquoted

    post = request.form
    userAgent = request.headers.get('User-Agent')
    target = request.url

    logMessage = "{0} {1}".format(
        request.method, target, get, post, userAgent)

    selectedRoute = None
    selectedPath = None
    for value in ROUTES:
        needle = path + getString(request)
        unquoted_needle = urllib.parse.unquote(needle)
        if path and path[0] != "." and value != "" and re.match(
                value, needle):
            selectedRoute = ROUTES[value]
            selectedPath = value
            break

    if selectedRoute is None and path == "":
        selectedRoute = ROUTES[""]
        selectedPath = ""

    if selectedRoute is not None:
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), logMessage, False, request.remote_addr, useragent=userAgent, get=unquoted_needle, post=post)
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
        logging.log(logging.EVENT_ID_HTTP_REQUEST, datetime.now(), logMessage, True, request.remote_addr, useragent=userAgent, get=unquoted_needle, post=post)
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

    downloadDir = config.getConfigurationValue("honeypot", "downloadDir")

    # if the download dir is not absolute, create a proper absolute path to avoid cwd issues
    if not isabs(downloadDir):
        downloadDir = join(config.ROOT, downloadDir)

    if not isdir(downloadDir):
        Path(downloadDir).mkdir(parents=True, exist_ok=True)
        logging.log(logging.EVENT_ID_DOWNLOAD_FOLDER_CREATE, datetime.now(), "Created download folder", not isdir(downloadDir), None)

    ROUTES = parseRoutes(routesFiles)
    app.run(
        debug=config.getConfigurationValue("honeypot", "debug"),
        host=config.getConfigurationValue("http", "host"),
        port=int(config.getConfigurationValue("http", "port"))
    )
