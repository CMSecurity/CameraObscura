# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Serves a given file as HTTP response
"""

import random
import re
from datetime import datetime
from os.path import join
import pathlib
from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageEnhance
from core import config, logging, http


def run(app: Flask, selectedPath: str, route: object,
        request: request):
    file = route["servefile"]["file"]
    if "(" in selectedPath:
        match = re.search(selectedPath, request.path)
        if match is not None:
            groups = match.groups()
            index = 1
            for group in groups:
                file = file.replace("$" + str(index), group)
                index = index + 1
    if isinstance(file, list):
        random.seed(datetime.now().time().microsecond)
        fileToServe = join(config.ROOT, file[random.randint(0, len(file) - 1)])
    else:
        fileToServe = join(config.ROOT, file)
    

    pathInfo = pathlib.Path(fileToServe)
    if "render_template" in route["servefile"] and route["servefile"]["render_template"] == True:
        getValues = http.getString(request)
        return render_template(
            route["servefile"]["file"], config=config, getValues=getValues, ip=request.remote_addr)
    if ".txt" in pathInfo.suffix:
        content = ""
        with open(fileToServe, 'r') as handle:
            content = handle.read()
            matches = re.findall(r"(\$[a-z\.]+)", content)
            if matches is not None:
                for match in matches:
                    name = match.replace("$", "")
                    value = ""
                    if "." in name:
                        parts = name.split(".")
                        value = config.getConfigurationValue(
                            parts[0], parts[1])
                    else:
                        variables = {
                            "day": datetime.now().day,
                            "hour": datetime.now().hour,
                            "minute": datetime.now().minute,
                            "month": datetime.now().month,
                            "second": datetime.now().second,
                            "year": datetime.now().year
                        }
                        if name in variables:
                            value = str(variables[name])
                    if value is not None:
                        content = content.replace(match, value)
        return content
    return send_file(fileToServe, as_attachment=False)
