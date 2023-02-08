import sqlite3

conn = sqlite3.connect('HorizonCinemaDB.db')

cur = conn.cursor()

def getCursor():
    return cur

def getConn():
    return conn