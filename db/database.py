import sqlite3, os

POKEDEX_DB = "pokedex.db"

def get_connection():
  connection = sqlite3.connect(POKEDEX_DB)
  connection.row_factory = sqlite3.Row
  return connection

def create_database():
  if os.path.exists(POKEDEX_DB):
    return

  connection = sqlite3.connect(POKEDEX_DB)
  cursor = connection.cursor()

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS pokemon (
  number INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  name_fr TEXT NOT NULL,
  types TEXT NOT NULL,
  image_url TEXT NOT NULL,
  height INTEGER NOT NULL,
  weight INTEGER NOT NULL,
  evolves_from_number INTEGER
  )
  """)

  connection.commit()
  connection.close()