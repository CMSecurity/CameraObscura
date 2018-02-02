from CameraTest import *
import unittest
import os
import sys


class TestConfig(CameraTest):
    def test_getConfigurationCorrectFile(self):
        file=os.path.join(self.parentDir,"configuration.cfg")
        
        from core import config
        got=config.getConfiguration(file)        

        self.assertNotEqual(got, None)

    def test_getConfigurationWrongFile(self):
        file=os.path.join(self.parentDir,"configuration.cfg_doesnotexists")
        
        from core import config
        got=config.getConfiguration(file)

        self.assertEqual(got, None)

    def test_getConfigurationValueCorrectValue(self):        
        from core import config
        got=config.getConfigurationValue("honeypot", "hostname")     
        self.assertEqual(got, "srv04.foo.bar")

    def test_getConfigurationValueWrongValue(self):        
        from core import config
        got=config.getConfigurationValue("honeypot", "hostname_doesnotexist")        

        self.assertEqual(got, None)

    def test_getConfigurationValueWrongSection(self):        
        from core import config
        got=config.getConfigurationValue("honeypot_doesnotexists", "hostname")        

        self.assertEqual(got, None)

if __name__ == '__main__':
    unittest.main()