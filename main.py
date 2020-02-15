# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Program main entrance point
"""

from os.path import isfile, join
from core import http, config

if isfile(join(config.ROOT, "configuration.cfg")) is False:
    raise Exception("configuration.cfg is missing")
else:
    http.serve(__file__)
