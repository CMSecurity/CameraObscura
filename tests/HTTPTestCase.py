import CameraTestCase
import unittest
import os
import sys
import datetime

class HTTPTestCase(CameraTestCase.CameraTestCase):
    def test_parseRoutes(self):
        from core import http
        got=http.parseRoutes("templates/ugly/routes.json")  

        self.assertNotEqual(got, None)
    
    def test_parseRoutesRoutesCheck(self):
        from core import http
        got=http.parseRoutes("templates/ugly/routes.json")  
        self.assertNotEqual(got["admin.php"], None)

    

if __name__ == '__main__':
    unittest.main()