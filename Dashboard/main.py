from DatabaseAccess import *
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/home") #Route for the about us page
@app.route("/")        
def aboutus():
   print("Home")
   return render_template("base.html")

if __name__ == "__main__":
   app.run(debug = True) #will run the flask app