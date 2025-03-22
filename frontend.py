import streamlit as st

st.title("Infinum JurisMind")

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