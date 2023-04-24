import unittest
from Db2 import *

from main import *

from datetime import datetime

import os


os.environ['DATABASE_URL'] = 'sqlite://'


class TestDatabase(unittest.TestCase):

    def test_connection(self):
        self.assertTrue(conn)


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['SECRET_KEY'] = 'hello'
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        self.client = self.app.test_client()


    def tearDown(self):
        self.app_ctxt.pop()
        self.app = None
        self.app_ctxt = None
        self.client = None


    def test_app(self):
        assert self.app is not None
        assert app == self.app

    #Test base render
    def test_base_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/'

    #Test home page render
    def test_home_redirect(self):
        response = self.client.get('/home', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/home'

    #Test players render
    def test_player_redirect(self):
        response = self.client.get('/players', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/players'

    #Test clubs render
    def test_clubs_redirect(self):
        response = self.client.get('/clubs', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/clubs'

    #Test specific player render
    def test_playersname_redirect(self):
        response = self.client.get('/players/NB009', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/players/NB009'

    #Test specific club render
    def test_clubsname_redirect(self):
        response = self.client.get('/clubs/REDNORTH', follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/clubs/REDNORTH'

    #Test login page render
    def test_login_page(self):
        response = self.client.get('/login')
        assert response.status_code == 200
        assert response.request.path == '/login'
        html = response.get_data(as_text=True)

        assert 'name="adminemail"' in html
        assert 'name="adminpassword"' in html

    #Testing correct credentials for admin page
    def test_admin_login(self):
        response = self.client.post('/login', data={
            'adminemail': 'admin@gmail.com',
            'adminpassword': 'admin123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == '/admin'

    #Testing incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post('/login', data={
            'adminemail': 'thisiswrong@gmail.com',
            'adminpassword': 'thisiswrongadmin123'
        }, follow_redirects=True)
        self.assertFalse(response.request.path == '/admin')


class TestMainProgram(unittest.TestCase):

    # Test for getting weeks left
    def test_weeksleft(self):

        self.weeksleft = getWeeksLeftInContract(playerStartOfContract = "01/01/2019", playerContractDuration = 5)

        print(self.weeksleft)

        currentDate = datetime.now()
        currentDate = currentDate.strftime("%d/%m/%Y")
        currentDate = datetime.strptime(currentDate, "%d/%m/%Y")

        print("Todays Date: ", currentDate)

        playerStartOfContractAsDate = datetime.strptime("01/01/2019", '%d/%m/%Y')

        #Get the weeks the player has already played of his contract
        playerWeeksPlayedOfContract = (currentDate - playerStartOfContractAsDate).days
        playerWeeksPlayedOfContract = playerWeeksPlayedOfContract // 7
        #Get the weeks the player has over his entire contract
        playerWeeksInContract = ((5 * 365) // 7)
        #Find the difference between them for the remaining weeks in players contract
        playerWeeksLeftInContract = playerWeeksInContract - playerWeeksPlayedOfContract

        self.assertEqual(self.weeksleft, playerWeeksLeftInContract)

    # Test for Market Value calculation being correct
    def test_marketcalculation(self):
        
        self.marketvalue = calculatePrices(playerSalary = 100000, playerGamesWon = 10, playerWeeksLeftInContract = 10, playerGamesPlayedThisYear = 20, playerFutureGames = "WWWLL")

        print(self.marketvalue[0])

        expected = [500000, 471428.5714285715, 436363.63636363635, 395652.17391304346, 325000.0, 260000.0] # Salary, FG1, FG2, FG3, FG4, FG5

        self.assertEqual(self.marketvalue, expected)

if __name__ == '__main__':
    unittest.main()