import sqlite3
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


playerHeadings = ['Player Number','Player Name', 'Date of Birth', 'Gender', 'Date Signed-Up', 'Current Team', 'Team Location', 'Team Manager', 'Salary (£k/Week)', 'Start of Contract', 'Contract Duration', 'Games Played This Year', 'Games Won', 'Future Games']
clubHeadings = ['Club Name', 'Club Location', 'Club Manager']

def calculateCurrentPrice(playerSalary, playerWeeksLeftInContract, playerBaseWinRate):
   return (playerSalary * playerWeeksLeftInContract * playerBaseWinRate)

def calculateFuturePrices(playerSalary, playerGamesWon, playerGamesPlayedThisYear, playerWeeksLeftInContract, playerFutureGames):
   playerFuturePrices = []
   for i in range(len(playerFutureGames)):
      if playerFutureGames == 'W':
         playerGamesWon += 1
         playerGamesPlayedThisYear += 1
         playerWeeksLeftInContract -= 1
      else:
         playerGamesPlayedThisYear += 1
         playerWeeksLeftInContract -= 1

      newWinRate = playerGamesWon / playerGamesPlayedThisYear
      priceAfterGame = playerSalary * playerWeeksLeftInContract * newWinRate
      playerFuturePrices.append(priceAfterGame)
   return playerFuturePrices

@app.route("/home") #Route for the about us page
@app.route("/")        
def home():
   print("Home")
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players")
      data = cur.fetchall()
   conn.close()
   return render_template("home.html", data = data[0])

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
   return render_template("clubs.html", clubHeadings = clubHeadings)

@app.route("/players/<playerID>")
def playerDetails(playerID):
   print("Player Details")
   print(playerID)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players WHERE player_ID = ?", (playerID,))
      playerInfo = cur.fetchall()
      print(playerInfo)
      playerName = playerInfo[0][1]
      playerDoB = playerInfo[0][2]
      playerGender = playerInfo[0][3]
      playerDateSignedUp = playerInfo[0][4]
      playerCurrentTeam = playerInfo[0][5]
      playerTeamLocation = playerInfo[0][6]
      playerTeamManager = playerInfo[0][7]
      playerSalary = playerInfo[0][8]
      playerStartOfContract = playerInfo[0][9]
      playerContractDuration = playerInfo[0][10]
      playerGamesPlayedThisYear = playerInfo[0][11]
      playerGamesWon = playerInfo[0][12]
      playerFutureGames = playerInfo[0][13]
   #Convert salary to value in thousands (e.g. 50 becomes 50000)
   playerSalary = int(playerSalary) * 1000
   print(playerSalary)
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
   print(playerWeeksInContract)
   print(playerWeeksPlayedOfContract)
   #Find the difference between them for the remaining weeks in players contract
   playerWeeksLeftInContract = playerWeeksInContract - playerWeeksPlayedOfContract
   print(playerWeeksLeftInContract)
   #Get the win rate not based on any future games
   playerBaseWinRate = playerGamesWon / playerGamesPlayedThisYear
   print(playerBaseWinRate)
   #Get price of player before any future games
   playerCurrentPrice = calculateCurrentPrice(playerSalary, playerWeeksLeftInContract, playerBaseWinRate)
   print(playerCurrentPrice)
   #Get price of player after each future game
   playerFuturePrices = calculateFuturePrices(playerSalary, playerGamesWon, playerGamesPlayedThisYear, playerWeeksLeftInContract, playerFutureGames)
   print(playerFuturePrices)

   conn.close()
   return render_template('playerdetails.html', playerID = playerID, playerName = playerName, playerData= playerInfo, playerHeadings=playerHeadings)


if __name__ == "__main__":
   app.run(debug = True) #will run the flask app