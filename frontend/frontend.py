import streamlit as st
import requests
import random

st.title("Infinum JurisMind")

host='backend'

# Read style
with open("Style/main.css", "r") as f:
    css_content = f.read()

st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


# API response from history
try:
    response = requests.get(f'http://{host}:8000/history')  # History API endpoint
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

############################ Main part
# Because we can not use CSS position: sticky; to keep input field to follow scrolling
input_container = st.empty()

# Place for the user prompt
with input_container:
    user_prompt = st.chat_input("Enter your prompt", key="text_input")


st.sidebar.subheader("More options")

# Check if the user entered a prompt and handle it
if user_prompt:
    st.session_state.current_discussion.append(f"You: {user_prompt}")
    answer = "Not connected to API for chatbot"

    try:
        # Send a POST request with JSON body
        response = requests.post(f"http://{host}:8000/ask", json={"question": user_prompt})  
        if response.status_code == 200:
            answer = response.json().get('answer', 'ERROR!!!')
        else:
            answer = "Bad API"
    except Exception as e:
        answer = f"I can not answer due to connection error: {str(e)}"

    st.session_state.current_discussion.append(f"JurisMind: {answer}")

chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.current_discussion:
        if "You:" in msg:
            st.markdown(f"<p style='color: orange'>{msg}</p>", unsafe_allow_html=True)
        else:
            lines = msg.split("\n")
            for line in lines:
                st.markdown(f"<p style='color: white'>{line}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


if st.sidebar.button('New Chat'):
    try:
        # Check if selected chat exist
        if 'current_discussion' in st.session_state and st.session_state.current_discussion:
            # Save id
            title = st.session_state.current_discussion[0].split(":")[1].strip()
        else:
            # If chat does not exist, generate new id for new chat
            random_number = random.randint(1, 100000)
            title = f"Chat{random_number}"

        prompts = []
        for i in range(0, len(st.session_state.current_discussion), 2):
            question = st.session_state.current_discussion[i]
            answer = st.session_state.current_discussion[i + 1] if i + 1 < len(st.session_state.current_discussion) else ""
            prompts.append(question)
            prompts.append(answer)

        # Call API for saving chats and prompts
        response = requests.post(f"http://{host}:8000/save_prompt", json={  
            "title": title,
            "prompts": prompts
        })

        if response.status_code == 200:
            st.success("Prompts saved successfully.")
        else:
            st.error(f"Failed to save prompts: {response.status_code} - {response.text}")

        # Reset curr discussion
        st.session_state.current_discussion = []  
        
        # Refresh page
        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.current_discussion = []  
        st.rerun()





############################ Sidebar
# Sidebar where we would save the history of conversation
st.sidebar.title("History")


# Check if there are old chats
if st.session_state.history:
    for idx, chat in enumerate(st.session_state.history):
        chat_title = chat[0]  # Title from API

        if st.sidebar.button(f"{idx + 1}: {chat_title}"):
            try:
                response = requests.get(f"http://{host}:8000/history_chat", params={"title": chat_title})  # Fixed URL

                if response.status_code == 200:
                    chat_data = response.json()
                    #if len(st.session_state.current_discussion)>0:
                    
                    st.session_state.current_discussion = []  # Reset current discussion
                    
                    # Save old discussion to continue it
                    if isinstance(chat_data, list):
                        for msg in chat_data:
                            st.session_state.current_discussion.append(f"You: {msg['question']}")
                            st.session_state.current_discussion.append(f"JurisMind: {msg['answer']}")

                        # Print old prompts
                        st.rerun()

                    else:
                        st.sidebar.error("Invalid API response format")

                else:
                    st.sidebar.error(f"API error: {response.status_code}")

            except Exception as e:
                st.sidebar.error(f"Connection error: {str(e)}")
else:
    st.sidebar.write("Empty history")
