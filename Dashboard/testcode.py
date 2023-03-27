import unittest
from DatabaseAccess import *

from main import *

from datetime import datetime

from pytest import *

from conftest import *

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
    
    def test_index_route(self):
        # response = self.app.get('/')
        # self.assertEqual(response.status_code, 200)

        client = app.test_client
        response = client.get('/home')
        self.assertEqual(response.status_code, 200)

# class TestFlaskRoutes(unittest.TestCase):
#     def setUp(self):
#         app.testing = True
#         self.client = app.test_client()
    
#     def test_home(client):

#         client = app.test_client
#         response = client.get('/home')
#         assert(response.status_code, 200)

class TestDatabase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(conn)


class TestMainProgram(unittest.TestCase):

    # Test for getting weeks left
    def test_weeksleft(self):

        self.weeksleft = getWeeksLeftInContract(playerStartOfContract = "01/01/2019", playerContractDuration = 5)

        print(self.weeksleft)

        currentDate = datetime.now()
        currentDate = currentDate.strftime("%d/%m/%Y")
        currentDate = datetime.strptime(currentDate, "%d/%m/%Y")

        print("Todays Date: ", currentDate)

        expected = 40 # NOTE == CURRENTLY UNIT TEST WILL FAIL DUE TO TODAYS DATE CHANGING SO WEEKS LEFT CHANGING

        self.assertEqual(self.weeksleft, expected)

    # Test for Market Value calculation being correct
    def test_marketcalculation(self):
        
        self.marketvalue = calculatePrices(playerSalary = 100000, playerGamesWon = 10, playerWeeksLeftInContract = 10, playerGamesPlayedThisYear = 20, playerFutureGames = "WWWLL")

        print(self.marketvalue[0])

        expected = [500000, 471428.5714285715, 436363.63636363635, 395652.17391304346, 325000.0, 260000.0] # Salary, FG1, FG2, FG3, FG4, FG5

        self.assertEqual(self.marketvalue, expected)

class TestRoutes(unittest.TestCase):
    pass
# # Testing
    
#     def test_base_route(self):
#         app = Flask(__name__)

#         client = app.test_client()
#         url = '/'

#         response = client.get(url)
#         assert response.status_code == 200



class TestRoutes(unittest.TestCase):
    pass
    # def test_home(client):
    #     response = client.get("/")
    #     assert b"<title>Home</title>" in response.data


    # def test_request(client):
    #     c = Client(test_app)
    #     response = c.get("/")
    #     response.status_code

    #     print(response)



class TestLogin(unittest.TestCase):

    pass
    
    # def test_login(self):

    #     email = request.form["adminemail"]
    #     password = request.form["adminpassword"]

    #     assert email == 'admin@gmail.com'
    #     assert password != 'admin123'


        
    #     #self, 'admin@gmail.com', 'admin123'

    #     success = self.model = login()


class TestAdmin(unittest.TestCase):

    def add_player(self):
        
        pass

if __name__ == '__main__':
    unittest.main()