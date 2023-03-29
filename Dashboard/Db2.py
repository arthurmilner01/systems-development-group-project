#Arthur Milner 21035478
#Simply gets the database connection, same as examples given
import sqlite3

conn = sqlite3.connect('Mball2.db')

cur = conn.cursor()

def getCursor():
    return cur

def getConn():
    return conn