# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Catches uploaded files from HTTP POST requestObjs
"""

import hashlib
import os

from os.path import join, isdir, isfile, isabs
from datetime import datetime
from core import config, logging


def run(app, selectedPath: str, route: object,
        requestObj):
    """
    Executes the catchfile action
    """
    if requestObj.method == 'POST':
        for key in requestObj.files:
            file_object = requestObj.files.get(key)
            # shasum = hashlib.sha224(copy.copy(file_object).read()).hexdigest()
            filename = str(datetime.now().timestamp())
            downloadDir = config.getConfigurationValue("honeypot", "downloadDir")

            if not isabs(downloadDir):
                downloadDir = join(config.ROOT, downloadDir)
            if not isdir(downloadDir):
                raise Exception("Download dir not existing")

            file_path = join(downloadDir, filename)
            file_object.save(file_path)

            shasum = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    shasum.update(data)
            hashed_filepath = join(downloadDir, shasum.hexdigest())
            os.rename(file_path, hashed_filepath)

            logging.log(logging.EVENT_ID_UPLOAD,
                        datetime.now(),
                        "Uploaded {0}".format(shasum.hexdigest()),
                        not isfile(file_path),
                        requestObj.remote_addr,
                        shasum=shasum.hexdigest())
