import mysql.connector

# Open connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='chat' # My table
)

cursor=conn.cursor() # Interaction with the MySQL server

cursor.execute("SELECT * FROM chats")
cursor.fetchall()
cursor.close()

conn.close() # Close connection