import sqlite3

conn = sqlite3.connect("wallet.db")
cursor = conn.cursor()

cursor.execute(
    """
   CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY,
       username TEXT UNIQUE,
       email TEXT UNIQUE,
       hashed_password TEXT,
       disabled BOOLEAN
   )
"""
)

conn.commit()
conn.close()
