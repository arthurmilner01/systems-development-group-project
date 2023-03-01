from DatabaseAccess import *
import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


playerHeadings = ['Player Number','Player Name', 'Date of Birth', 'Gender', 'Date Signed-Up', 'Current Team', 'Team Location', 'Team Manager', 'Salary (£k/Week)', 'Start of Contract', 'Contract Duration', 'Games Played This Year', 'Games Won', 'Future Games']
clubHeadings = ['Club Name', 'Club Location', 'Club Manager']


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

@app.route("/players/<playerName>")
def playerDetails(playerName):
   print("Player Details")
   return render_template('playerdetails.html', playerName = playerName)


if __name__ == "__main__":
   app.run(debug = True) #will run the flask app