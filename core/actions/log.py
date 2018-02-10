# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Creates a log entry 
"""

from flask import Flask, request
from core import logging

def run(app: Flask, route: object, request: request, sessionId: str):
    logging.log(logging.EVENT_ID_HTTP, datetime.now(), "HTTP-{0} Request".format(request.method), "http", False, request.remote_addr,0.0, sessionId)