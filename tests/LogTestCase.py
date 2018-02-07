import CameraTestCase
import unittest
import os
import sys
import datetime

class LogTestCase(CameraTestCase.CameraTestCase):
    def test_Log(self):
        from core import logging
        got=logging.log(logging.EVENT_ID_STARTED,datetime.datetime.now(),"foo","bar",True,"",0.0,"foo")    
        self.assertEqual(got, True)

    def test_LogWrongType(self):
        from core import config, logging
        config.CONFIG["log"]["method"] = "thisisnotexisting"
       
        got=logging.log(logging.EVENT_ID_STARTED,datetime.datetime.now(),"foo","bar",True,"",0.0,"foo")    
        self.assertEqual(got, False)


if __name__ == '__main__':
    unittest.main()