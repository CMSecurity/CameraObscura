# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Program main entrance point
"""

import sys
from os.path import isfile, join
import termcolor
from core import http, config

if isfile(join(config.ROOT, "configuration.cfg")) is False:
    raise Exception("configuration.cfg is missing")
else:
    http.serve(__file__)
