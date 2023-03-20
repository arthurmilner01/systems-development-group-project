import unittest
from DatabaseAccess import *
from main import *



class TestDatabase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(conn)


class TestMainProgram(unittest.TestCase):

    # Test for getting weeks left
    def test_weeksleft(self):

        self.weeksleft = getWeeksLeftInContract(playerStartOfContract = "01/01/2019", playerContractDuration = 5)

        print(self.weeksleft)

        expected = 41

        self.assertEqual(self.weeksleft, expected)

    # Test for Market Value calculation being correct
    def test_marketcalculation(self):
        
        self.marketvalue = calculatePrices(playerSalary = 100000, playerGamesWon = 10, playerWeeksLeftInContract = 10, playerGamesPlayedThisYear = 20, playerFutureGames = "WWWLL")

        print(self.marketvalue[0])

        expected = [500000, 471428.5714285715, 436363.63636363635, 395652.17391304346, 325000.0, 260000.0] # Salary, FG1, FG2, FG3, FG4, FG5

        self.assertEqual(self.marketvalue, expected)

class TestRoutes(unittest.TestCase):
    
    pass

class TestLogin(unittest.TestCase):
    
    def test_login(self):
        
        #self, 'admin@gmail.com', 'admin123'

        success = self.model = login()


class TestAdmin(unittest.TestCase):

    def add_player(self):
        pass

if __name__ == '__main__':
    unittest.main()