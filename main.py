# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Program main entrance point
"""

from core import http, util
util.branding()
http.serve(__file__)