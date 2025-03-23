import psycopg2
from fastapi import FastAPI
import uvicorn
import openai
from pydantic import BaseModel
from typing import List 

# Init FastAPI
app = FastAPI()

# Function for connecting with PostgreSQL DB
def connect_to_db():
    return psycopg2.connect(
        host='localhost',  
        user='postgres',
        password='2000',  
        database='infinum_chat'
    )

# Retrieving history from DB
@app.get("/history")
async def get_history():
    conn = connect_to_db()    # Open connection with DB
    cursor = conn.cursor()    # Init cursor

    cursor.execute("SELECT title FROM chat")  # Execute PostgreSQL query
    results = cursor.fetchall()  # Take results

    cursor.close()  
    conn.close()  # Close connection

    return ([row[0]] for row in results)


@app.get("/history_chat")  # Save old prompts from chat
async def get_history_chat(title: str):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
        SELECT p.id, c.title, p.question, p.answer 
        FROM prompt p 
        JOIN chat c ON p.chat = c.id 
        WHERE c.title = %s
    """
    cursor.execute(query, (title,))  
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{"id": row[0], "title": row[1], "question": row[2], "answer": row[3]} for row in results]


class Prompt(BaseModel):
    title: str
    prompts: List[str]

# Save current prompt
@app.post("/save_prompt")
async def save_prompts(prompt: Prompt):
    title = prompt.title
    prompts = prompt.prompts
    
    conn = connect_to_db()
    cursor = conn.cursor()
    
    try:
        # Insert chat entry and get the chat_id using RETURNING
        insert_chat = "INSERT INTO chat (title) VALUES (%s) RETURNING id"
        cursor.execute(insert_chat, (title,))
        chat_id = cursor.fetchone()[0]  # Get the chat_id from RETURNING

        for i in range(0, len(prompts), 2):  
            question = prompts[i]
            answer = prompts[i + 1] if i + 1 < len(prompts) else ""  

            # Insert prompt and connect it with the chat_id
            insert_prompt = """
                INSERT INTO prompt (question, answer, chat) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_prompt, (question, answer, chat_id))
        
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    
    finally:
        cursor.close()
        conn.close()

    return {"message": "Prompts saved successfully"}


### Connect to OPENAI
client = openai.OpenAI(api_key='YOURAPIKEY')  # Connect to OpenAI with your API key

def ask_LLM(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal advisor. Only respond to legal questions related to law, contracts, rights, and legal procedures. If the question is not related to legal topics, respond with 'I can only answer legal questions related to law, contracts, rights, and legal procedures.'"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# API endpoint for bot response
@app.get("/ask")
async def get_answer(prompt: str):
    answer = ask_LLM(prompt)
    return {"question": prompt, "answer": answer}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
