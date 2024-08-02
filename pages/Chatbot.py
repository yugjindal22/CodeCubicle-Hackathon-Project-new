import os
import time
from threading import Timer
import streamlit as st
import platform
from PIL import Image
from Backend import interpret_command_with_gpt, process_interpreted_command, writeAssistantResponse

PAGE_ID = "platform_assistant"

# Reset chat history if page is switched
if "page_id" not in st.session_state or st.session_state.page_id != PAGE_ID:
    st.session_state.page_id = PAGE_ID
    st.session_state.messages = []
    st.session_state.show_chatbot = False

st.title("Platform Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False

if st.button("Start Chatting"):
    st.session_state.show_chatbot = True
    response = f"Hi there, I'm Platform Assistant. You can ask me anything related to our platform."
    st.session_state.messages.append({"role": "A", "content": response})

if st.session_state.show_chatbot:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Text input handling
    if prompt := st.chat_input("What is up?"):
        with st.chat_message("user"):
            st.markdown(f"You: {prompt}")
        st.session_state.messages.append({"role": "user", "content": f"You: {prompt}"})
        
        interpreted_command = interpret_command_with_gpt(prompt)
        process_interpreted_command(interpreted_command)
