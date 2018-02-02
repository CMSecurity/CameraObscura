import os
import sys
import unittest

class CameraTest(unittest.TestCase):
    parentDir=os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    def __init__(self, *args, **kwargs):
      unittest.TestCase.__init__(self, *args, **kwargs)
      sys.path.insert(0, self.parentDir)