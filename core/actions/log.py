# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Creates a log entry
"""

import datetime
from flask import Flask, request
from core import logging


def run(app, selectedPath: str, route: object,
        requestObj, sessionId: str):
    """
    Executes the logging action
    """
    logging.log(
        logging.EVENT_ID_HTTP,
        datetime.datetime.now(),
        "{0} Request".format(
            requestObj.method),
        "http",
        False,
        requestObj.remote_addr,
        0.0,
        sessionId)
