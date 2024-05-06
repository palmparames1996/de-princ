import sqlite3
import os

dbfile = os.environ['DB_FILE']

def connection_fileDB(dbfile = dbfile):
    return sqlite3.connect(dbfile)

def query_fileDB(query, dbfile = dbfile):
    # Create a SQL connection to our SQLite database
    con = connection_fileDB(dbfile)
    
    # Creating cursor
    cur = con.cursor()
    
    # Get data
    cur.execute(query)
    data = cur.fetchall()
    columns = [i[0] for i in cur.description]
    
    # Be sure to close the connection
    con.close()
    return {'data':data,'columns':columns}