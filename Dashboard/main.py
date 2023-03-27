import re
import sqlite3
from flask import Flask, render_template, session, flash, redirect, request, url_for, abort
from datetime import datetime
from werkzeug.security import check_password_hash
import random

app = Flask(__name__)
app.secret_key = "hello"


playerHeadings = ['Player Number','Player Name', 'Date of Birth', 'Gender', 'Date Signed-Up', 'Current Team', 'Salary (£k/Week)', 'Start of Contract', 'Contract Duration', 'Games Played This Year', 'Games Won', 'Future Games']
clubHeadings = ['Club ID', 'Club Name', 'Club Location', 'Club Manager']

def calculatePrices(playerSalary, playerGamesWon, playerWeeksLeftInContract, playerGamesPlayedThisYear, playerFutureGames):
   playerPrices = []
   baseWinRate = playerGamesWon / playerGamesPlayedThisYear
   basePrice = playerSalary * playerWeeksLeftInContract * baseWinRate
   playerPrices.append(basePrice)
   for i in range(len(playerFutureGames)):
      if playerFutureGames[i] == 'W':
         playerGamesWon += 1
         playerGamesPlayedThisYear += 1
         playerWeeksLeftInContract -= 1
      else:
         playerGamesPlayedThisYear += 1
         playerWeeksLeftInContract -= 1

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

def checkFirstVisit():
   if session.get("FirstVisit") == None:
      session["FirstVisit"] = True
   else:
      session["FirstVisit"] = False

def checkLoggedIn():
   if session.get("currentUserEmail") ==  None: #Redirects to error page if user is not admin
      print("User not admin, restricting access to this page.")
      abort(403)


@app.route("/home") #Route for the home page
@app.route("/")        
def home():
   print("Home")
   checkFirstVisit()
   with sqlite3.connect('MoneyballDB.db') as conn:
      cur = conn.cursor()
      cur.execute("SELECT player_name, current_team, future_games FROM players WHERE future_games LIKE '%W%' AND (length(future_games) - length(replace(future_games, 'W', ''))) = (SELECT MAX(length(future_games) - length(replace(future_games, 'W', ''))) FROM players) ORDER BY player_name ASC;")
      result = cur.fetchall()
   conn.close()
   print(f"The player with the most amount of wins is {result[0]} in {result[0]} with {result[1]} wins.")
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute('''SELECT * FROM Players ORDER BY RANDOM() LIMIT 5''')
      data = cur.fetchall()
   conn.close()
   trendingPlayers = []
   for i in range(5):
      playerWeeksLeftInContract = getWeeksLeftInContract(data[i][7], data[i][8])
      trendingPlayers.append(calculatePrices((data[i][6])*1000, data[i][10], playerWeeksLeftInContract, data[i][9], data[i][11]))
      for j in range(len(trendingPlayers[i])):
         trendingPlayers[i][j] = round(trendingPlayers[i][j], 2)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Clubs")
      clubData = cur.fetchall()
      playersByClub = []
      for club in clubData:    
         cur.execute("SELECT player_name, salary, start_of_contract, contract_duration, games_played_this_year, games_won, future_games FROM Players WHERE current_team = ?", (club[1],))
         players = cur.fetchall()
         players.append(club[1])
         playersByClub.append(players) 
      clubs = []
      for club in playersByClub:
         print(club)
         clubValues = [0,0,0,0,0,0, club[-1]]
         for i in range(len(club)-1):
            playerWeeksLeftInContract = getWeeksLeftInContract(club[i][2], club[i][3])
            playerPrices = calculatePrices((club[i][1] * 1000), club[i][5], playerWeeksLeftInContract, club[i][4], club[i][6])
            for i in range(len(playerPrices)):
               clubValues[i] = clubValues[i] + round(playerPrices[i])
         clubs.append(clubValues)
      clubs = sorted(clubs)
      clubs = clubs[-6:]
      week0 = []
      week1 = []
      week2 = []
      week3 = []
      week4 = []
      week5 = []
      for club in clubs:
         week0.append(club[0])
         week1.append(club[1])
         week2.append(club[2])
         week3.append(club[3])
         week4.append(club[4])
         week5.append(club[5])  
         
   photo = random.randint(1,6)
   return render_template("home.html",photo=photo, result=result, name1 = data[0][1], name2 = data[1][1], name3 = data[2][1], name4 = data[3][1], name5 = data[4][1], player1 = trendingPlayers[0], player2 = trendingPlayers[1], player3 = trendingPlayers[2], player4 = trendingPlayers[3], player5 = trendingPlayers[4], playerToWatch = data[0], week0 = week0, week1 = week1, week2 = week2, week3 = week3, week4 = week4, week5 = week5, club1 = clubs[0][6], club2 = clubs[1][6], club3 = clubs[2][6], club4 = clubs[3][6], club5 = clubs[4][6], club6 = clubs[5][6])

@app.route("/players") #Route for the players page        
def players():
   print("Players")
   checkFirstVisit()
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players")
      playerData = cur.fetchall()
   conn.close()
   return render_template("players.html", playerHeadings = playerHeadings, playerData=playerData)

@app.route("/clubs") #Route for the clubs page        
def clubs():
   print("Clubs")
   checkFirstVisit()
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Clubs")
      clubData = cur.fetchall()
   conn.close()
   return render_template("clubs.html", clubHeadings = clubHeadings, clubData=clubData)

@app.route("/players/<playerName>")
def playerDetails(playerName):
   print("Player Details")
   checkFirstVisit()
   print(playerName)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Players WHERE player_name = ?", (playerName,))
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
   
   photo = random.randint(1,7)
   
   return render_template('playerdetails.html', playerName = playerName, playerDoB = playerDoB,\
                           playerGender = playerGender, playerDateSignedUp = playerDateSignedUp, playerCurrentTeam = playerCurrentTeam,\
                           playerTeamLocation = playerTeamLocation, playerTeamManager = playerTeamManager, playerSalary = playerSalary,\
                           playerStartOfContract = playerStartOfContract, playerContractDuration = playerContractDuration,\
                           playerGamesPlayedThisYear = playerGamesPlayedThisYear, playerGamesWon = playerGamesWon, playerFutureGames = playerFutureGames,\
                           playerWeeksLeftInContract = playerWeeksLeftInContract, playerPrices = playerPrices, photo = photo)

@app.route("/clubs/<clubName>")
def clubDetails(clubName):
   print("Club Details")
   checkFirstVisit()
   print(clubName)
   with sqlite3.connect('MoneyballDB.db') as conn:      
      cur = conn.cursor()
      cur.execute("SELECT * FROM Clubs WHERE club_name = ?", (clubName,))
      clubData = cur.fetchone()      
      cur.execute("SELECT player_name, salary, start_of_contract, contract_duration, games_played_this_year, games_won, future_games, player_ID FROM Players WHERE current_team = ?", (clubName,))
      players = cur.fetchall()
      clubValues = [0,0,0,0,0,0]
      playerSalaries = []
      playerNames = []
      playerValuesDefault = []
      playerValues1 = ''
      playerValues2 = ''
      playerValues3 = ''
      playerValues4 = ''
      playerValues5 = ''
      for player in players:
         playerSalaries.append((player[1] * 1000))
         playerNames.append(player[7])
         playerWeeksLeftInContract = getWeeksLeftInContract(player[2], player[3])
         playerPrices = calculatePrices((player[1] * 1000), player[5], playerWeeksLeftInContract, player[4], player[6])
         playerValues1=playerValues1+str(playerPrices[0])+','
         playerValues2=playerValues2+str(playerPrices[1])+','
         playerValues3=playerValues3+str(playerPrices[2])+','
         playerValues4=playerValues4+str(playerPrices[3])+','
         playerValues5=playerValues5+str(playerPrices[4])+','
         playerValuesDefault.append(playerPrices[0])
         for i in range(len(playerPrices)):
            clubValues[i] = clubValues[i] + playerPrices[i]
      print(clubValues)
      print(playerNames)
      
         

   conn.close()


   return render_template('clubdetails.html', clubName = clubName, clubData = clubData, clubValues = clubValues, playerValuesDefault = playerValuesDefault ,playerSalaries=playerSalaries, playerNames=playerNames, playerValues1=playerValues1, playerValues2=playerValues2, playerValues3=playerValues3, playerValues4=playerValues4, playerValues5=playerValues5)


@app.route("/login", methods=["POST", "GET"]) #Route for the players page        
def login():
   print("Login")
   checkFirstVisit()
   if request.method == "POST":
      email = request.form["adminemail"]
      password = request.form["adminpassword"]
      print(email)
      print(password)
      with sqlite3.connect('MoneyballDB.db') as conn:      
         cur = conn.cursor()
         cur.execute("SELECT * FROM Users WHERE email = ?", (email,))
         results = cur.fetchone()
         if results != None:
            print("Account Found")
            cur.execute("SELECT password FROM Users WHERE email = ?", (email,))
            hashedPassword = cur.fetchone()
            hashedPassword = "".join(hashedPassword)
            print(hashedPassword)
            if check_password_hash(hashedPassword, password) == True:
               session["currentUserEmail"] = email
               return redirect(url_for("adminpage"))
            else:
               print("Incorrect password")
               flash("Error: Password was incorrect.")
               return redirect(url_for("login"))
         else:
            print("Account not found.") 
            flash("Error: Email has not been recognised.")
            return redirect(url_for("login"))
   elif request.method == "GET": #Will run when user presses log-out button, this clears the current session variables concerned with being logged-in
      if session.get("currentUserEmail") != None:
         print("Clearing session variables.")
         flash("User successfully logged out.")
         session.pop("currentUserEmail",None)
      return render_template("login.html")

@app.route("/admin", methods=["POST", "GET"])
def adminpage():
   print("Admin Page")
   checkLoggedIn()
   checkFirstVisit()
   if request.method == "POST":
      formName = request.form['form-adminpage']
      if formName == "add-player-form":
         with sqlite3.connect('MoneyballDB.db') as conn:
            cur = conn.cursor()
            playerName = request.form["player-name-add"].upper()
            playerDOB = request.form["player-dob-add"].upper()
            playerGender = request.form["player-gender-add"].upper()
            playerDSU = request.form["player-dsu-add"].upper()
            playerClubName = request.form["player-club-name-add"].upper()
            playerSalary = request.form["player-salary-add"].upper()
            playerSOC = request.form["player-soc-add"].upper()
            playerContractDuration = request.form["player-contract-duration-add"].upper()
            playerGamesPlayed = request.form["player-games-played-add"].upper()
            playerGamesWon = request.form["player-games-won-add"].upper()
            playerFutureGames = request.form["player-future-games-add"].upper()
            print(playerName)
            print(playerDOB)
            print(playerGender)
            print(playerDSU)
            print(playerClubName)
            print(playerSalary)
            print(playerSOC)
            print(playerContractDuration)
            print(playerGamesPlayed) 
            print(playerGamesWon)  
            print(playerFutureGames)
            # VALIDATION
            if re.search(r"^([A-Z]{2})([\d]{3})$", playerName) == None:      
               flash("Incorrect name format: " + str(playerName))
               return redirect(url_for("adminpage"))  
            date_format = "%Y-%m-%d"  
            correct_format = '%d/%m/%Y'
            now = datetime.now()
            now = now.strftime(correct_format)
            now = datetime.strptime(now, correct_format)            
            compareDate = datetime.strptime(playerDOB, date_format)
            playerDOB = compareDate.strftime(correct_format) 
            if compareDate > now:
               flash("Date of birth in future: " + str(playerDOB))
               return redirect(url_for("adminpage"))
            compareDate = datetime.strptime(playerDSU, date_format)
            playerDSU = compareDate.strftime(correct_format) 
            if compareDate > now:
               flash("Date signed up in future: " + str(playerDSU))
               return redirect(url_for("adminpage"))
            compareDate = datetime.strptime(playerSOC, date_format)
            playerSOC = compareDate.strftime(correct_format) 
            if compareDate > now:
               flash("Start of contract in future: " + str(playerSOC))
               return redirect(url_for("adminpage"))
            if re.search(r"^[0-9]+$", playerSalary) == None:
               flash("Incorrect salary format : " + str(playerSalary))
               return redirect(url_for("adminpage"))
            if re.search(r"^[0-9]+$", playerContractDuration) == None:
               flash("Incorrect contract duration format : " + str(playerContractDuration))
               return redirect(url_for("adminpage"))
            if re.search(r"^[0-9]+$", playerGamesPlayed) == None:
               flash("Incorrect games played format : " + str(playerGamesPlayed))
               return redirect(url_for("adminpage"))
            if re.search(r"^[0-9]+$", playerGamesWon) == None:
               flash("Incorrect games won format : " + str(playerGamesWon))
               return redirect(url_for("adminpage"))
            if re.search(r"^[WLD]{5}$", playerFutureGames) == None:
               flash("Incorrect future games format : " + str(playerFutureGames))
               return redirect(url_for("adminpage"))
            cur.execute("SELECT * FROM Players WHERE player_name = ?",(playerName,))
            result = cur.fetchone()
            if result == None:
               cur.execute("INSERT INTO Players (player_name, date_of_birth, gender, date_signed_up, current_team, salary, start_of_contract, contract_duration, games_played_this_year, games_won, future_games) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (playerName, playerDOB, playerGender, playerDSU, playerClubName, playerSalary, playerSOC, playerContractDuration, playerGamesPlayed, playerGamesWon, playerFutureGames))
               conn.commit()
               flash("Player Added.")
               return redirect(url_for("adminpage"))
            else:
               flash("Player name already found. Check player name")
               return redirect(url_for("adminpage"))
            
      elif formName == "del-player-form":
         with sqlite3.connect('MoneyballDB.db') as conn: 
            cur = conn.cursor()
            playerName = request.form["player-name-del"]
            cur.execute("SELECT * FROM Players WHERE player_name = ?", (playerName, ))
            result = cur.fetchone()
            if result != None:
               cur.execute("DELETE FROM Players WHERE player_name = ?", (playerName, ))
               conn.commit()
               flash("Player deleted.")
               return redirect(url_for("adminpage"))
            else:
               flash("Player not found. Did you select a player from the dropdown?")
               return redirect(url_for("adminpage"))
      elif formName == "add-club-form":
         with sqlite3.connect('MoneyballDB.db') as conn:
            cur = conn.cursor()
            clubName = request.form["club-name-add"].upper()
            clubLocation = request.form["club-location-add"].upper()
            clubManager = request.form["club-manager-add"].upper()
            print(clubName)
            print(clubLocation)
            print(clubManager)
            cur.execute("SELECT * FROM Clubs WHERE club_name = ?",(clubName,))
            result = cur.fetchone()
            if result == None:
               cur.execute("INSERT INTO Clubs (club_name, club_location, club_manager) VALUES (?,?,?)", (clubName, clubLocation, clubManager))
               conn.commit()
               flash("Club " + clubName + " inserted with manager " + clubManager + " and located in " + clubLocation + ".")
               return redirect(url_for("adminpage"))
            else:
               flash("That club name already exists.")
               return redirect(url_for("adminpage"))
      elif formName == "del-club-form":
         with sqlite3.connect('MoneyballDB.db') as conn: 
            cur = conn.cursor()
            clubName = request.form["club-name-del"]
            print(clubName)
            cur.execute("SELECT * FROM Clubs WHERE club_name = ?", (clubName, ))
            clubExists = cur.fetchone()
            print(clubExists)
            if clubExists != None:
               cur.execute("DELETE FROM Players WHERE current_team = ?", (clubName, ))
               cur.execute("DELETE FROM Clubs WHERE club_name = ?", (clubName, ))
               conn.commit()
               flash("Club and players for that club deleted.")
               return redirect(url_for("adminpage"))
            else:
               flash("Club not found. Did you select a club from the dropdown?")
               return redirect(url_for("adminpage"))
   elif request.method == "GET": #Will run when user presses log-out button, this clears the current session variables concerned with being logged-in
      with sqlite3.connect('MoneyballDB.db') as conn: 
         cur = conn.cursor()
         cur.execute("SELECT club_name FROM Clubs ORDER BY club_name ASC")
         clubNameList = cur.fetchall()
         cur.execute("SELECT player_name FROM Players ORDER BY player_name ASC")
         playerNameList = cur.fetchall()
      return render_template("adminpage.html", clubNameList = clubNameList, playerNameList = playerNameList)

@app.errorhandler(403)
def error403(error):
   return render_template("403error.html"), 403

if __name__ == "__main__":
   app.run(debug = True) #will run the flask app