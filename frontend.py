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
    st.session_state.history = []   # Initialize history in session



############################Main part
# Place for the user prompt
user_prompt=st.text_input("You: ")




############################Sidebar
# Sidebar where we would save history of conversation
st.sidebar.title("History")


# Check if there are old chats
if st.session_state.history:
    for i in st.session_state.history:
        chat=f'<a href="#">Chat</a>'
else:
    st.sidebar.write("Empty history")