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

if st.button('End chat'):
    if st.session_state.current_discussion:
        st.session_state.history.append(st.session_state.current_discussion)
        st.session_state.current_discussion = []  # Reset chat


############################Sidebar
# Sidebar where we would save history of conversation
st.sidebar.title("History")



# Check if there are old chats
# Check if there are old chats
if st.session_state.history:
    for idx, chat in enumerate(st.session_state.history):
        chat_title = chat[0]  # Naslov iz API-ja

        if st.sidebar.button(f"{idx + 1}: {chat_title}"):
            try:
                response = requests.get("http://127.0.0.1:8000/history_chat", params={"title": chat_title})
                if response.status_code == 200:
                    chat_data = response.json()
                    st.session_state.current_discussion = [f"You: {msg['question']}\nJurisMind: {msg['answer']}" for msg in chat_data]
                else:
                    st.sidebar.error("Could not load chat history")
            except Exception as e:
                st.sidebar.error(f"Error loading chat: {str(e)}")
else:
    st.sidebar.write("Empty history")
