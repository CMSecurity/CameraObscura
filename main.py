# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Program main entrance point
"""

from core import http, util, config, init
import termcolor
import sys
from os.path import isfile, join
util.branding()
if len(sys.argv) == 2 and sys.argv[1] == "init":
  init.init()
  sys.exit(0)

if isfile(join(config.ROOT, "configuration.cfg")) == False:
  print(termcolor.colored("We recommend to initalize the honeypot to generate different serial numbers, versions and model numbers.", "yellow"))
  print("You can do this with python3 main.py init")
else:
  http.serve(__file__)