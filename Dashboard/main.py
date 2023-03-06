import sqlite3
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


playerHeadings = ['Player Number','Player Name', 'Date of Birth', 'Gender', 'Date Signed-Up', 'Current Team', 'Salary (£k/Week)', 'Start of Contract', 'Contract Duration', 'Games Played This Year', 'Games Won', 'Future Games']
clubHeadings = ['Club Name', 'Club Location', 'Club Manager']

def calculatePrices(playerSalary, playerGamesWon, playerWeeksLeftInContract, playerGamesPlayedThisYear, playerFutureGames):
   playerPrices = []
   baseWinRate = playerGamesWon / playerGamesPlayedThisYear
   basePrice = playerSalary * playerWeeksLeftInContract * baseWinRate
   playerPrices.append(basePrice)
   for i in range(len(playerFutureGames)):
      if playerFutureGames[i] == 'W':
         playerGamesWon += 1
         playerGamesPlayedThisYear += 1
      else:
         playerGamesPlayedThisYear += 1

      newWinRate = playerGamesWon / playerGamesPlayedThisYear
      priceAfterGame = playerSalary * playerWeeksLeftInContract * newWinRate
      playerPrices.append(priceAfterGame)
   return playerPrices

def getWeeksLeftInContract(playerStartOfContract, playerContractDuration):
   #Get current date in desired format
   currentDate = datetime.now()
   currentDate = currentDate.strftime("%d/%m/%Y")
   currentDate = datetime.strptime(currentDate, "%d/%m/%Y")
   #Get start of contract in desired format
   playerStartOfContractAsDate = datetime.strptime(playerStartOfContract, '%d/%m/%Y')
   #Get the weeks the player has already played of his contract
   playerWeeksPlayedOfContract = (currentDate - playerStartOfContractAsDate).days
   playerWeeksPlayedOfContract = playerWeeksPlayedOfContract // 7
   #Get the weeks the player has over his entire contract
   playerWeeksInContract = ((playerContractDuration * 365) // 7)
   #Find the difference between them for the remaining weeks in players contract
   playerWeeksLeftInContract = playerWeeksInContract - playerWeeksPlayedOfContract
   return playerWeeksLeftInContract

@app.route("/home") #Route for the about us page
@app.route("/")        
def home():
   print("Home")
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute('''SELECT * FROM Players ORDER BY RANDOM() LIMIT 5''')
      data = cur.fetchall()
   conn.close()
   trendingPlayers = []
   player1 = data[0][1]
   player2 = data[1][1]
   player3 = data[2][1]
   player4 = data[3][1]
   player5 = data[4][1]
   for i in range(5):
      playerWeeksLeftInContract = getWeeksLeftInContract(data[i][7], data[i][8])
      trendingPlayers.append(calculatePrices(data[i][6]*1000, data[i][10], playerWeeksLeftInContract, data[i][9], data[i][11]))
      for j in range(len(trendingPlayers[i])):
         trendingPlayers[i][j] = round(trendingPlayers[i][j], 2)
   print(trendingPlayers[0])
   return render_template("home.html", player1Data = trendingPlayers[0], player2Data = trendingPlayers[1], playerToWatch = data[0], player1 = player1, player2 = player2, player3 = player3, player4 = player4, player5 = player5)

@app.route("/players") #Route for the players page        
def players():
   
   print("Players")
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players")
      playerData = cur.fetchall()
   conn.close()
   return render_template("players.html", playerHeadings = playerHeadings, playerData=playerData)

@app.route("/clubs") #Route for the clubs page        
def clubs():
   print("Clubs")
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Clubs")
      clubData = cur.fetchall()
   conn.close()
   return render_template("clubs.html", clubHeadings = clubHeadings, clubData=clubData)

@app.route("/players/<playerID>")
def playerDetails(playerID):
   print("Player Details")
   print(playerID)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players WHERE player_ID = ?", (playerID,))
      playerInfo = cur.fetchone()
      print(playerInfo)
      playerName = playerInfo[1]
      playerDoB = playerInfo[2]
      playerGender = playerInfo[3]
      playerDateSignedUp = playerInfo[4]
      playerCurrentTeam = playerInfo[5]
      playerSalary = playerInfo[6]
      playerStartOfContract = playerInfo[7]
      playerContractDuration = playerInfo[8]
      playerGamesPlayedThisYear = playerInfo[9]
      playerGamesWon = playerInfo[10]
      playerFutureGames = playerInfo[11]
      cur.execute("SELECT club_location, club_manager FROM Clubs WHERE club_name = ?", (playerCurrentTeam, ))
      clubInfo = cur.fetchone()
      playerTeamLocation = clubInfo[0]
      playerTeamManager = clubInfo[1]
   #Convert salary to value in thousands (e.g. 50 becomes 50000)
   playerSalary = int(playerSalary) * 1000
   print(playerSalary)
   playerWeeksLeftInContract = getWeeksLeftInContract(playerStartOfContract, playerContractDuration)
   #Get price of player and price after each future game
   playerPrices = calculatePrices(playerSalary, playerGamesWon, playerWeeksLeftInContract, playerGamesPlayedThisYear, playerFutureGames)
   print(playerPrices)
   for i in range(len(playerPrices)):
      playerPrices[i] = round(playerPrices[i], 2)
   print(playerPrices)

   conn.close()
   return render_template('playerdetails.html', playerID = playerID, playerName = playerName, playerDoB = playerDoB,\
                           playerGender = playerGender, playerDateSignedUp = playerDateSignedUp, playerCurrentTeam = playerCurrentTeam,\
                           playerTeamLocation = playerTeamLocation, playerTeamManager = playerTeamManager, playerSalary = playerSalary,\
                           playerStartOfContract = playerStartOfContract, playerContractDuration = playerContractDuration,\
                           playerGamesPlayedThisYear = playerGamesPlayedThisYear, playerGamesWon = playerGamesWon, playerFutureGames = playerFutureGames,\
                           playerWeeksLeftInContract = playerWeeksLeftInContract, playerPrices = playerPrices)

@app.route("/clubs/<clubID>")
def clubDetails(clubID):
   print("Club Details")
   print(clubID)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Clubs WHERE club_name = ?", (clubID,))
      clubData = cur.fetchone()      
      cur.execute("SELECT player_name, salary, start_of_contract, contract_duration, games_played, games_won, future_games FROM Players WHERE current_team = ?", (clubID,))
      players = cur.fetchall()
      conn.close()
   clubValues = []
   for player in players:
      pass


   return render_template('clubdetails.html', clubID = clubID, clubData = clubData, players = players)


if __name__ == "__main__":
   app.run(debug = True) #will run the flask app