# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Program main entrance point
"""

import sys
from os.path import isfile, join
import termcolor
from core import http, config, init

if len(sys.argv) == 2 and sys.argv[1] == "init":
    init.init()
    sys.exit(0)

if isfile(join(config.ROOT, "configuration.cfg")) is False:
    print(termcolor.colored("We recommend to initalize the honeypot", "yellow"))
    print("You can do this with python3 main.py init")
else:
    http.serve(__file__)
