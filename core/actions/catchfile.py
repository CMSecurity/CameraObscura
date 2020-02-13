# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Catches uploaded files from HTTP POST requestObjs
"""

from shutil import move
from os import path, remove
from os.path import join, isdir, isfile
from datetime import datetime
from flask import request
from core import config, util, logging
import random
import string

def getRandomFilename():
    """
    Returns a random string file name
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(25))


def run(app, selectedPath: str, route: object,
        requestObj):
    """
    Executes the catchfile action
    """
    if requestObj.method == 'POST':
        for key in requestObj.files:
            file_object = requestObj.files.get(key)
            file_name = getRandomFilename()
            workDir = config.getConfigurationValue("honeypot", "downloadDir")
            if not isdir(workDir):
                raise Exception("Download dir not existing")
            file_path = join(workDir, file_name)
            if isfile(file_path):
                raise Exception("File already existing")
            file_object.save(file_path)
            logging.log(logging.EVENT_ID_UPLOAD,
                        datetime.now(),
                        "Downloaded {0}".format(file_name),
                        not isfile(file_path),
                        requestObj.remote_addr)
    return None
