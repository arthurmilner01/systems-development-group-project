import unittest
from DatabaseAccess import *
from main import *


class TestDatabase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(conn)


class TestLogin(unittest.TestCase):
    
    def test_login(self):
        pass


class TestAdmin(unittest.TestCase):

    def add_player(self):
        pass

if __name__ == '__main__':
    unittest.main()