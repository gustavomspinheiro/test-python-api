import sqlite3

connection = sqlite3.connect('test.db')
cursor = connection.cursor()

createUsers = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(createUsers)

createItems = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(createItems)


connection.commit()
connection.close()
