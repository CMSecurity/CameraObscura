# Copyright (c) 2018 RoastingMalware
# See the LICENSE file for more information

import hashlib

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