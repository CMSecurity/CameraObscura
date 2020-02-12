# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

"""
Misc. functionality used by several modules
"""

from os.path import join
from sys import version
import hashlib
import termcolor
from core import config, constants

def getChecksum(filename: str) -> str:
    """
    Returns the checksum for a given file
    """
    blocksize = 65536
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(blocksize), b''):
            sha256.update(block)
    return sha256.hexdigest()
