import sqlite3


connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', 
               ('newuser', 'newuser@example.com', 28))
cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', 
               ('user1', 'newuser1@example.com', 25))

connection.commit()

cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

for user in users:
    print(user)
    
connection.close()
