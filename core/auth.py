# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
This module contains auth related functionality
"""

import re

class Credentials():
  userName=""
  password=""
  isForbidden=False
  def __init__(self, userName: str, password: str, isForbidden: bool):
    self.userName = userName
    self.password = password
    self.isForbidden = isForbidden

def isAuthorized(userName: str, password: str) -> bool:
  content = ""
  a = open("userdb.txt","r")
  lineRegex=r"(?P<username>[^:]+):x:(?P<password>.+)"
  p = re.compile(lineRegex)
  successfull = True
  while True:
    line = a.readline()
    parts = line.split(":x:")
    if len(parts) == 2:
      lineUser = parts[0]
      linePw = parts[1].strip() # strip because of trailing \n 
      forbidden=linePw[0] == "!"
      if forbidden:
        linePw = linePw[1:] # strip the ! out of the password
      
      # case one the password is listed and not forbidden
      if lineUser == userName and linePw == password and forbidden == False:
        successfull = True
        break
      
      if lineUser == userName and linePw == password and forbidden == True:
        print("foo")
        successfull = False
        break

      if lineUser == userName and linePw == "*":
        successfull = True
        break

    if not line: 
        break

  a.close()
  return successfull