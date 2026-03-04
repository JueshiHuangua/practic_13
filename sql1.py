import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

connection.close()
