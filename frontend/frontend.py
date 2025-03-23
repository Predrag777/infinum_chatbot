import streamlit as st
import requests
import random

st.title("Infinum JurisMind")

# API response from history
try:
    response = requests.get('http://backend:8000/history')  # History API endpoint
    if response.status_code == 200:
        api_history = response.json()
        st.session_state.history = api_history
    else:
        st.error("Can not connect to server")
except Exception as e:
    st.error(f"Server error: {str(e)}")

# Save discussion history
if 'history' not in st.session_state:
    st.session_state.history = []  # Initialize global history in session

# Save current discussion
if 'current_discussion' not in st.session_state:
    st.session_state.current_discussion = []

############################Main part
# Place for the user prompt
user_prompt = st.text_input("You: ")

if user_prompt:
    st.session_state.current_discussion.append(f"You: {user_prompt}")
    answer = "Not connected to API for chatbot"

    try:
        # Send a POST request with JSON body
        response = requests.post("http://backend:8000/ask", json={"question": user_prompt})
        if response.status_code == 200:
            answer = response.json().get('answer', 'ERROR!!!')
        else:
            answer = "Bad API"
    except Exception as e:
        answer = f"I can not answer due to connection error: {str(e)}"

    st.session_state.current_discussion.append(f"JurisMind: {answer}")

    # Display the conversation
    for msg in st.session_state.current_discussion:
        if "You" in msg:
            st.markdown(f"<p style='color: blue'>{msg}</p>", unsafe_allow_html=True)
        elif 'JurisMind' in msg:
            st.markdown(f"<p style='color: green'>{msg}</p>", unsafe_allow_html=True)


# Close and save chat in history
if st.button('End chat'):
    try:
        random_number = random.randint(1, 100000)
        title = f"Chat{random_number}"

        prompts = []
        for i in range(0, len(st.session_state.current_discussion), 2):
            question = st.session_state.current_discussion[i]
            answer = st.session_state.current_discussion[i + 1] if i + 1 < len(st.session_state.current_discussion) else ""
            prompts.append(question)
            prompts.append(answer)

        # Send data to the backend API to save it in DB
        response = requests.post("http://backend:8000/save_prompt", json={  # Fixed URL
            "title": title,
            "prompts": prompts
        })

        if response.status_code == 200:
            st.success("Prompts saved successfully.")
        else:
            st.error(f"Failed to save prompts: {response.status_code} - {response.text}")

        # Add the current discussion to history and reset the current discussion
        st.session_state.history.append(st.session_state.current_discussion)
        st.session_state.current_discussion = []  # Reset chat

    except Exception as e:
        st.error(f"Error: {str(e)}")
        # If there's an error, still add the current discussion to history and reset
        st.session_state.history.append(st.session_state.current_discussion)
        st.session_state.current_discussion = []  # Reset chat

############################Sidebar
# Sidebar where we would save the history of conversation
st.sidebar.title("History")

# Check if there are old chats
if st.session_state.history:
    for idx, chat in enumerate(st.session_state.history):
        chat_title = chat[0]  # Title from API

        if st.sidebar.button(f"{idx + 1}: {chat_title}"):
            try:
                response = requests.get(f"http://backend:8000/history_chat", params={"title": chat_title})  # Fixed URL

                if response.status_code == 200:
                    chat_data = response.json()
                    st.session_state.current_discussion = []  # Reset current discussion

                    # Save old discussion to continue it
                    if isinstance(chat_data, list):
                        for msg in chat_data:
                            st.session_state.current_discussion.append(f"You: {msg['question']}")
                            st.session_state.current_discussion.append(f"JurisMind: {msg['answer']}")

                        # Print old prompts
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