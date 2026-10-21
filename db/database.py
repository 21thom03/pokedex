import sqlite3

def get_connection():
  connection = sqlite3.connect("database.db")
  connection.row_factory = sqlite3.Row
  try :
    yield connection
    connection.commit()
  finally:
    connection.close()