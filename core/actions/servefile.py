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
from core import config, http
from PIL import ImageDraw, Image

def run(app: Flask, selectedPath: str, route: object,
        request: request):
    file = route["servefile"]["file"]
    variables = {
        "day": datetime.now().day,
        "hour": datetime.now().hour,
        "minute": datetime.now().minute,
        "month": datetime.now().month,
        "second": datetime.now().second,
        "year": datetime.now().year,
        "date": str(datetime.now())
    }
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
                        if name in variables:
                            value = str(variables[name])
                    if value is not None:
                        content = content.replace(match, value)
        return content
    watermark = "watermark" in route["servefile"]
    if watermark:
        watermark_obj = route["servefile"]["watermark"]
        x_coord = watermark_obj["x"]
        y_coord = watermark_obj["y"]
        text = watermark_obj["text"]
        im = Image.open(fileToServe)
        
        if text in variables:
            text = str(variables[text])
        ImageDraw.Draw(
         im 
        ).text(
            (x_coord, y_coord),  # Coordinates
            text,
            (0, 0, 0)  # Color
        )
        mime = im.get_format_mimetype()
        format = im.format
        response = None
        im.save(fileToServe + "obscura", format)
        response = send_file(fileToServe + "test", mimetype=mime, as_attachment=False,attachment_filename="image")
        return response
    return send_file(fileToServe, as_attachment=False)
