import psycopg2
from fastapi import FastAPI
import uvicorn
import openai
from pydantic import BaseModel
from typing import List 
from langchain_community.chat_models import ChatOpenAI  
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain


# Init FastAPI
app = FastAPI()

# Function for connecting with PostgreSQL DB
def connect_to_db():
    return psycopg2.connect(
        host='postgres',  
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


@app.get("/history_chat")  # Retreive prompts from old chat
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

# Save chat and its prompts
@app.post("/save_prompt")
async def save_prompts(prompt: Prompt):
    title = prompt.title
    prompts = prompt.prompts
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        # Check if id of current chat exist
        cursor.execute("SELECT id FROM chat WHERE title = %s", (title,))
        chat_row = cursor.fetchone()
        
        if chat_row:
            chat_id = chat_row[0]  
        else:
            # If chat does not exist, create new row in db
            insert_chat = "INSERT INTO chat (title) VALUES (%s) RETURNING id"
            cursor.execute(insert_chat, (title,))
            chat_id = cursor.fetchone()[0] 

        # Save chat prompts
        for i in range(0, len(prompts), 2):  
            question=prompts[i]
            answer=prompts[i+1] if i+1<len(prompts) else ""  
            insert_prompt="""
                INSERT INTO prompt (question, answer, chat) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(insert_prompt,(question,answer,chat_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
    return {"message": "Prompts saved successfully"}


# Provide your API key
my_key="YOUR_API_KEY"

# We want to provide answer only for the legal questions.
template = """You are a legal advisor. Only respond to legal questions related to law, contracts, rights, and legal procedures. If the question is not related to legal topics, respond with 'I can only answer legal questions related to law, contracts, rights, and legal procedures.'
Chat history: {history}
Question: {input}"""

# Crete template for prompts
prompt = ChatPromptTemplate.from_template(template)

# Init memory
memory = ConversationBufferMemory(memory_key="history")

# Init chat
chat = ChatOpenAI(model="gpt-4", api_key=my_key)

# Init COnversationChain
conversation_chain = ConversationChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=True
)

class QuestionRequest(BaseModel):
    question: str

# API endpoint for chat responses
@app.post("/ask")
async def get_answer(request: QuestionRequest):
    try:
        answer = conversation_chain.run({"input": request.question})
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}

# Run 
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)