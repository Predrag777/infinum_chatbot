import streamlit as st
import requests






st.title("Infinum JurisMind")


# API response from history
try:
    response = requests.get('http://127.0.0.1:8000/history') # History API endpoint
    if response.status_code == 200:
        api_history = response.json()  
        st.session_state.history = api_history  
    else:
        st.error("Can not connect to server")
except Exception as e:
    st.error(f"Server error: {str(e)}")



# Save discussion history
if 'history' not in st.session_state:
    st.session_state.history = []   # Initialize global history in session

# Save current discussion
if 'current_discussion' not in st.session_state:
    st.session_state.current_discussion=[]

############################Main part
# Place for the user prompt
user_prompt=st.text_input("You: ")

if user_prompt:
    st.session_state.current_discussion.append(f"You: {user_prompt}")
    answer = "Not connected to API for chatbot"

    try:
        response = requests.get("http://127.0.0.1:8000/ask", params={"prompt": user_prompt})  # Use user_prompt, not user_input
        if response.status_code == 200:
            answer = response.json().get('answer', 'ERROR!!!')
        else:
            answer = "Bad API"
    except Exception as e:
        answer = f"I can not answer due to connection error: {str(e)}"

    st.session_state.current_discussion.append(f"JurisMind: {answer}")

    for msg in st.session_state.current_discussion:
        if "You" in msg:
            st.markdown(f"<p style='color: blue'>{msg}</p>", unsafe_allow_html=True)
        elif 'JurisMind' in msg:
            st.markdown(f"<p style='color: green'>{msg}</p>", unsafe_allow_html=True)


import random
import requests

if st.button('End chat'):
    try:
        # Generišemo nasumičan broj između 1 i 100
        random_number = random.randint(1, 100)

        # Kreiramo title u formatu "ChatX"
        title = f"Chat{random_number}"

        # Pretvorimo trenutnu diskusiju u listu pitanja i odgovora
        prompts = []
        for i in range(0, len(st.session_state.current_discussion), 2):
            question = st.session_state.current_discussion[i]
            answer = st.session_state.current_discussion[i + 1] if i + 1 < len(st.session_state.current_discussion) else ""
            prompts.append(question)
            prompts.append(answer)

        # Debugging: Ispisivanje sadržaja koji šaljemo
        print(f"Title: {title}")
        print(f"Prompts: {prompts}")

        # Poziv API-ja sa generisanim title i listom prompts kao JSON
        response = requests.post("http://127.0.0.1:8000/save_prompt", json={
            "title": title,
            "prompts": prompts
        })

        if response.status_code == 200:
            st.success("Prompts saved successfully.")
        else:
            st.error(f"Failed to save prompts: {response.status_code} - {response.text}")

        # Dodaj trenutnu diskusiju u istoriju i resetuj trenutnu diskusiju
        st.session_state.history.append(st.session_state.current_discussion)
        st.session_state.current_discussion = []  # Reset chat

    except Exception as e:
        st.error(f"Error: {str(e)}")
        # Ako dođe do greške, još uvek dodaj trenutnu diskusiju u istoriju i resetuj
        st.session_state.history.append(st.session_state.current_discussion)
        st.session_state.current_discussion = []  # Reset chat


############################Sidebar
# Sidebar where we would save history of conversation
st.sidebar.title("History")



# Check if there are old chats
if st.session_state.history:
    for idx, chat in enumerate(st.session_state.history):
        chat_title = chat[0]  # Title from API

        if st.sidebar.button(f"{idx + 1}: {chat_title}"):
            try:
                response = requests.get("http://127.0.0.1:8000/history_chat", params={"title": chat_title})
                

                if response.status_code == 200:
                    chat_data = response.json()
                    st.session_state.current_discussion = [] # Reset current discussion

                    # Save old discussion to continue it
                    if isinstance(chat_data, list):
                        for msg in chat_data:
                            st.session_state.current_discussion.append(f"You: {msg['question']}")
                            st.session_state.current_discussion.append(f"JurisMind: {msg['answer']}")

                        # Print old discussion
                        for msg in st.session_state.current_discussion:
                            if "You" in msg:
                                st.markdown(f"<p style='color: blue'>{msg}</p>", unsafe_allow_html=True)
                            elif 'JurisMind' in msg:
                                st.markdown(f"<p style='color: green'>{msg}</p>", unsafe_allow_html=True)
                    else:
                        st.sidebar.error("Invalid API response format")
                    
                else:
                    st.sidebar.error(f"API error: {response.status_code}")
                
            except Exception as e:
                st.sidebar.error(f"Connection error: {str(e)}")
else:
    st.sidebar.write("Empty history")