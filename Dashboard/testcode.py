import unittest
from DatabaseAccess import *
from main import *


class TestDatabase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(conn)

class TestMain(unittest.TestCase):

    # Test for getting weeks left
    def test_getweeksleft():
        pass

    # Test for Market Value calculation being correct
    def test_calculation(self):

        success = self.model = calculatePrices(50, 11, 40, 22, "WWLWD") #Salary, Games won, Weeks left, Games Played, Future games
        self.assertEqual(success, 1200000)
        # self.assertEqaul(playerPrices, ) #what it equals

class TestLogin(unittest.TestCase):
    
    def test_login(self):
        pass


class TestAdmin(unittest.TestCase):

    def add_player(self):
        pass

if __name__ == '__main__':
    unittest.main()