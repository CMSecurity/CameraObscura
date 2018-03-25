# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Catches uploaded files from HTTP POST requests
"""

from flask import request,  Flask
from core import config, util, logging
from shutil import move
from os import path, remove
from os.path import join
from datetime import datetime


def run(app: Flask, selectedPath: str, route: object,
        request: request, sessionId: str):
    if request.method == 'POST':
        for key in request.files:
            file = request.files.get(key)
            if file.filename != "":
                workdir = config.getConfigurationValue("honeypot", "workdir")
                tmpFile = path.join(workdir, file.filename)
                file.save(tmpFile)
                hash = util.getChecksum(tmpFile)
                dlPath = path.join(app.config['UPLOAD_FOLDER'], hash)
                if path.isfile(dlPath) == False:
                    move(tmpFile, dlPath)
                    logging.log(logging.EVENT_ID_UPLOAD,
                                datetime.now(),
                                "File {0} uploaded to dl/{1}".format(file.filename,
                                                                     hash),
                                "http",
                                False,
                                request.remote_addr,
                                0.0,
                                sessionId)
                else:
                    remove(tmpFile)
                    logging.log(
                        logging.EVENT_ID_UPLOAD,
                        datetime.now(),
                        "Not storing duplicate content {1}".format(
                            file.filename,
                            hash),
                        "http",
                        False,
                        request.remote_addr,
                        0.0,
                        sessionId)
    return None
