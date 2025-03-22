import streamlit as st

st.title("Infinum JurisMind")

# Place for the user prompt
user_prompt=st.text_input("You: ")


# Sidebar where we would save history of conversation
st.sidebar.title("History")