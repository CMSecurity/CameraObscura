import CameraTestCase
import unittest
import os
import sys
import datetime

class AuthTestCase(CameraTestCase.CameraTestCase):
    def test_isAuthorizedBlacklistedPW(self):
        from core import auth
        got=auth.isAuthorized("root","root")

        self.assertNotEqual(got, True)

    def test_isAuthorizedNonBlacklistedPw(self):
        from core import auth
        got=auth.isAuthorized("root","root2")

        self.assertEqual(got, True)

    def test_isAuthorizedNotlistedUser(self):
        from core import auth
        got=auth.isAuthorized("notlisted","root2")

        self.assertEqual(got, True)

    def test_isAuthorizedEmptyPasswordAndUser(self):
        from core import auth
        got=auth.isAuthorized("","")

        self.assertEqual(got, False)
    
if __name__ == '__main__':
    unittest.main()