# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Serves a given file as HTTP response
"""

from datetime import datetime
from os.path import join
import pathlib
from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageEnhance
from core import config, logging, http
import random

def run(app: Flask, route: object, request: request, sessionId: str):
  file = route["servefile"]["file"]
  
  if isinstance(file, list):
    random.seed(datetime.now().time()) 
    fileToServe = join(config.ROOT,file[random.randint(0, len(file) -1)])
  else:
    fileToServe = join(config.ROOT,file)
  
  pathInfo = pathlib.Path(fileToServe)
  if "watermark" in route["servefile"] and route["servefile"]["watermark"] and pathInfo.suffix.replace(".","") in config.getConfigurationValue("image","images").replace(r"\s","").split(","):
    tmpPath =join(config.getConfigurationValue("image","workdir"), pathInfo.name + pathInfo.suffix)
    now = datetime.now().isoformat()
    original = Image.open(fileToServe)
    watermark = Image.new("RGBA", original.size)
    waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
    waterdraw.text((4, 2), "%s %s" % (config.getConfigurationValue("image","watermark"), now))
    original.paste(watermark, None, watermark)
    original.save(tmpPath)
    return send_file(tmpPath, as_attachment=False)
  if "render_template" in route["servefile"] and route["servefile"]["render_template"] == True:
    getValues = http.getString(request)
    return render_template(route["servefile"]["file"], config=config, getValues=getValues)
  return send_file(fileToServe, as_attachment=False)