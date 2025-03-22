import mysql.connector
from fastapi import FastAPI
import uvicorn
import openai

#Init FastAPI
app=FastAPI()

def connect_to_db():
    return  mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='chat' # My table
    )

# Retrieving history from DB
@app.get("/history")
async def get_history():
    conn=connect_to_db()    # Open connection with DB
    cursor=conn.cursor()    # init cursor

    cursor.execute("SELECT * FROM chats") # Execute MYSQL prompt
    results=cursor.fetchall() # Take results

    cursor.close()  
    conn.close()    # Close connection

    return ([row[0], row[1], row[2], row[3]] for row in results)




client = openai.OpenAI(api_key="YOUR-KEY")
# 
def ask_LLM(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal advisor."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/ask")
async def get_answer(prompt:str):
    answer=ask_LLM(prompt)
    return {"question": prompt, "answer": answer}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)