# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Catches uploaded files from HTTP POST requestObjs
"""

from shutil import move
from os import path, remove
from os.path import join
from datetime import datetime
from flask import request
from core import config, util, logging


def run(app, selectedPath: str, route: object,
        requestObj, sessionId: str):
    """
    Executes the catchfile action
    """
    if requestObj.method == 'POST':
        for key in requestObj.files:
            file = requestObj.files.get(key)
            if file.filename != "":
                workdir = config.getConfigurationValue("honeypot", "workdir")
                tmpFile = join(workdir, file.filename)
                file.save(tmpFile)
                hashcode = util.getChecksum(tmpFile)
                dlPath = join(app.config['UPLOAD_FOLDER'], hashcode)
                if path.isfile(dlPath) is False:
                    move(tmpFile, dlPath)
                    logging.log(logging.EVENT_ID_UPLOAD,
                                datetime.now(),
                                "File {0} uploaded to dl/{1}".format(file.filename,
                                                                     hashcode),
                                "http",
                                False,
                                requestObj.remote_addr,
                                0.0,
                                sessionId)
                else:
                    remove(tmpFile)
                    logging.log(
                        logging.EVENT_ID_UPLOAD,
                        datetime.now(),
                        "Not storing duplicate content {1}".format(file.filename),
                        "http",
                        False,
                        requestObj.remote_addr,
                        0.0,
                        sessionId)
    return None
