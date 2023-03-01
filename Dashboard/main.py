from DatabaseAccess import *
from flask import Flask, render_template



playerHeadings = ['Player Name', 'Date of Birth', 'Gender', 'Date Signed-Up', 'Current Team', 'Team Location', 'Team Manager', 'Salary (£k/Week)', 'Start of Contract', 'Contract Duration', 'Games Played This Year', 'Games Won', 'Future Games']
clubHeadings = ['Team Name', 'Team Location', 'Team Manager']

    


app = Flask(__name__)

@app.route("/home") #Route for the about us page
@app.route("/")        
def home():
   print("Home")
   return render_template("home.html")

@app.route("/players") #Route for the players page        
def players():
   print("Players")
   return render_template("players.html")

@app.route("/clubs") #Route for the clubs page        
def clubs():
   print("Clubs")
   return render_template("clubs.html")

if __name__ == "__main__":
   app.run(debug = True) #will run the flask app