import sqlite3

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

try:
    cursor.execute('BEGIN')
    
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', 
                   ('user3', 'user3@example.com'))
    cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', 
                   ('user4', 'user4@example.com'))
    
    cursor.execute('COMMIT')
    
except:
    cursor.execute('ROLLBACK')

connection.commit()
connection.close()
