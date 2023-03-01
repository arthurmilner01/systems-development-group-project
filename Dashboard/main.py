from DatabaseAccess import *
from flask import Flask, render_template
import csv
import os

absolutePath = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(absolutePath, "Players_File.csv"), "r") as csvFile:
    reader = csv.reader(csvFile)
    


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