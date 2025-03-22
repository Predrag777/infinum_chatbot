import streamlit as st
import requests

st.title("Infinum JurisMind")


# API response from history
try:
    response = requests.get('http://127.0.0.1:8000/history') # History API endpoint
    if response.status_code == 200:
        api_history = response.json()  
        st.session_state.global_history = api_history  
    else:
        st.error("Can not connect to server")
except Exception as e:
    st.error(f"Server error: {str(e)}")



# Save discussion history
if 'global_history' not in st.session_state:
    st.session_state.global_history = []   # Initialize global history in session

if 'history' not in st.session_state:
    st.session_state.history=[]

############################Main part
# Place for the user prompt
user_prompt=st.text_input("You: ")

if user_prompt:
    st.session_state.history.append(f"You: {user_prompt}")
    answer="Not connected to APi for chatbot"

    st.session_state.history.append(f'JurisMind: {answer}')

    for msg in st.session_state.history:
        if "You" in msg:
            st.markdown(f"<p style='color: blue'>{msg}</p>", unsafe_allow_html=True)
        elif 'JurisMind' in msg:
            st.markdown(f"<p style='color: green'>{msg}</p>", unsafe_allow_html=True)

if st.button('End chat'):
    if st.session_state.history:
        st.session_state.global_history.append(st.session_state.history)
        st.session_state.history = []  # Reset chat


############################Sidebar
# Sidebar where we would save history of conversation
st.sidebar.title("History")



# Check if there are old chats
if st.session_state.global_history:
    for idx, chat in enumerate(st.session_state.global_history):
        chat_text = f"Chat {idx + 1}: {chat[1]} -> {chat[2]}" # Answer from API
        st.sidebar.markdown(f'<a href="javascript:void(0);" onclick="window.parent.location.hash=\'chat{idx}\'">{chat_text}</a>', unsafe_allow_html=True)
else:
    st.sidebar.write("Empty history")