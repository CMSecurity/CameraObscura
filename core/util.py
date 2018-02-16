# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

import hashlib
from core import config
from os import read
from os.path import join
import termcolor
from sys import version


"""
Misc. functionality used by several modules
"""

def getChecksum(filename: str) -> str:
  blocksize=65536
  sha256 = hashlib.sha256()
  with open(filename, 'rb') as f:
    for block in iter(lambda: f.read(blocksize), b''):
        sha256.update(block)
  return sha256.hexdigest()

def branding() -> str:
  if config.getConfigurationValue("honeypot","branding"):
    print("Camera Obscura [{0}, Python {1}]- https://github.com/roastingmalware/cameraobscura".format(termcolor.colored(getVersion(), 'yellow'),version))
    print("Hans, get ze {0}".format(termcolor.colored("Flammenwerfer", 'red', 'on_white')))
  debugModeEnabled = config.getConfigurationValue("honeypot","debug")
  if debugModeEnabled == True:
    print(termcolor.colored("For god's sake, disable the debug mode!", 'red'))

def getVersion() -> str:
  versionPath = join(config.ROOT, ".git/refs/heads/master")
  version = None
  with open(versionPath, 'r') as file:
    version = file.read()

  return version.strip()