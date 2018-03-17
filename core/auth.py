# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains auth related functionality
"""

from os.path import join
from core import config

def isAuthorized(userName: str, password: str) -> bool:
    """
    Tries to authentificate the given username and password based on the local userdb
    """
    if userName == "" or password == "":
        return False
    a = open(join(config.ROOT, "userdb.txt"), "r")
    successfull = True
    while True:
        line = a.readline()
        parts = line.split(":x:")
        if len(parts) == 2:
            lineUser = parts[0]
            linePw = parts[1].strip()  # strip because of trailing \n
            forbidden = linePw[0] == "!"
            if forbidden:
                linePw = linePw[1:]  # strip the ! out of the password

            # case one the password is listed and not forbidden
            if lineUser == userName and linePw == password and forbidden is False:
                successfull = True
                break

            if lineUser == userName and linePw == password and forbidden is True:
                successfull = False
                break

            if lineUser == userName and linePw == "*":
                successfull = True
                break

        if not line:
            break

    a.close()
    return successfull
