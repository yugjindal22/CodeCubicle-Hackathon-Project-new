import os
import time
from threading import Timer
import streamlit as st
from PIL import Image
from Backend import interpret_command_with_gpt, process_interpreted_command

PAGE_ID = "design_feedback_bot"

# Reset chat history if page is switched
if "page_id" not in st.session_state or st.session_state.page_id != PAGE_ID:
    st.session_state.page_id = PAGE_ID
    st.session_state.messages = []
    st.session_state.show_chatbot = False

st.title("Design Feedback Bot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False

if st.button("Start Chatting"):
    st.session_state.messages = []
    st.session_state.show_chatbot = True
    response = "Hi there, I'm Design Feedback Bot. How can I assist you?"
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
        
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": "Uploaded an image."})
        
        # Get feedback on the image
        result = interpret_command_with_gpt(image)
        process_interpreted_command(result)
        
        # Prompt the user to upload another image
        st.session_state.show_chatbot = False
        if st.button("Upload another image for feedback"):
            st.session_state.show_chatbot = True
