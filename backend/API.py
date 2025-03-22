import mysql.connector
from fastapi import FastAPI
import uvicorn

#Init FastAPI
app=FastAPI()

def connect_to_db():
    return  mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='chat' # My table
    )

@app.get("/history")
async def get_history():
    conn=connect_to_db()    # Open connection with DB
    cursor=conn.cursor()    # init cursor

    cursor.execute("SELECT * FROM chats") # Execute MYSQL prompt
    results=cursor.fetchall() # Take results

    cursor.close()  
    conn.close()    # Close connection

    return ([row[0], row[1], row[2], row[3]] for row in results)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)