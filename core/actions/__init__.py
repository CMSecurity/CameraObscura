# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

from core import logging
from datetime import datetime

"""
Main management entry point for http actions
"""

__all__ = [
    'catchfile',
    'servefile',
    'text',
    'authorize',
    'sleep',
    'log'
]


def isAllowed(action: str):
    return action in __all__


def run(action, app, path, route, request, sessionId):
    if isAllowed(action) == False:
        logging.log(
            logging.EVENT_ID_ACTION_NOT_FOUND,
            datetime.now(),
            "Action not found {0}".format(action),
            "http",
            True,
            request.remote_addr,
            0.0,
            sessionId)
        return None
    modules = globals()
    if action in modules:
        return modules[action].run(app, path, route, request, sessionId)
    return None
