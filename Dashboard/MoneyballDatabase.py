from DatabaseAccess import *
import csv
import os
from werkzeug.security import generate_password_hash

playerData = []

absolutePath = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(absolutePath, "Players_File.csv"), "r") as csvFile:
    reader = csv.reader(csvFile)
    i =0 
    for line in reader:
        if i != 0: 
            playerData.append(line)
        i = 1

print(playerData)



cur = getCursor()
conn = getConn()

# Dropping tables if they exist
cur.execute('''
DROP TABLE if exists Players
''')

cur.execute('''
DROP TABLE if exists Clubs
''')

cur.execute('''
DROP TABLE if exists Users
''')

#Creating Tables

cur.execute('''
CREATE TABLE Clubs
(club_ID INTEGER PRIMARY KEY, club_name varchar(120) UNIQUE NOT NULL, club_location varchar(120) NOT NULL, club_manager varchar(120) NOT NULL)
''')

cur.execute('''
CREATE TABLE Players
(player_ID INTEGER PRIMARY KEY, player_name varchar(120) UNIQUE NOT NULL, date_of_birth DATE NOT NULL, gender char(1) NOT NULL, 
date_signed_up DATE NOT NULL, current_team varchar(120) NOT NULL , salary INT NOT NULL, start_of_contract DATE NOT NULL, 
contract_duration INT NOT NULL, games_played_this_year INT NOT NULL, games_won INT NOT NULL,
future_games char(5) NOT NULL)
''')

cur.execute('''
CREATE TABLE Users
(user_ID INTEGER PRIMARY KEY, email varchar(120) UNIQUE NOT NULL, password varchar(120) NOT NULL)
''')

checkedClubs = []

for player in playerData:
    playerFutureGames = ''
    for i in range(12, 17):
        playerFutureGames += str(player[i])
    if player[4] not in checkedClubs:
        checkedClubs.append(player[4])
        query = """
        INSERT INTO Clubs(club_name, club_location, club_manager)
        VALUES (?, ?, ?)
        """
        cur.execute(query, (player[4], player[5], player[6]))
    # Insert into Players table
    query = """INSERT INTO Players(player_name, date_of_birth, gender, date_signed_up, current_team, salary, start_of_contract, contract_duration, games_played_this_year,
    games_won, future_games)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(query, (player[0], player[1], player[2], player[3], player[4], player[7], player[8], player[9], player[10], player[11], playerFutureGames))

    

password = generate_password_hash("admin123", method="sha256")

query = """
INSERT INTO Users(email, password)
VALUES(?, ?)
"""
cur.execute(query, ("admin@gmail.com", password))

conn.commit()