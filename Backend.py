import json
import time
import google.generativeai as genai
import platform
import streamlit as st
import PIL.Image
from PIL import Image


def interpret_command_with_gpt(command):

    api_key = st.secrets["api_keys"]["genai"]
    genai.configure(api_key= api_key)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    
    img = PIL.Image.open('tshirt.JPG')

    prompt_parts = f"""
        
        Interpret the following command and provide the output in JSON format, dont explain anything:
        
        input: Hello how are you?
        output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "I'm great, thank you! How can I assist you today?",
        }}
        }}

        input: What is this platform for?
        output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "This is an innovative platform that bridges the gap between designers and manufacturers. 
        Designers can post their creations for manufacturers to purchase, and there's also a marketplace 
        where customers can buy directly from designers and manufacturers. Additionally, the platform helps 
        designers connect with manufacturers to produce their designs, fostering a collaborative and efficient ecosystem for 
        creative ideas and production solutions.",
        }}
        }}

        input: what all can you do?
        output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "I can answer any questions that you might have about our platform, and I can even give you feedback on your designs! If you want feedback on a design, just say \"I want design feedback\".",
        }}
        }}

        
        input: Who are you?
        
        output: {{
        "action": "general_chat",
        "parameters": {{
            "response": "I'm your FashionTech Assistant, here to help you navigate our platform and connect with designers and manufacturers.",
        }}
        }}


        input: I want design feedback
        output: {{
        "action": "judge_image",
        "parameters": {{
            "response": "please upload an image for me to judge"
        }}
        }}

        input: Please rate my design
        output: {{
        "action": "judge_image",
        "parameters": {{
            "response": "please upload an image for me to judge"
        }}
        }}
        
        input: {img}
        output: {{
        "action": "image_input",
        "parameters": {{
            "response": "The design is clean and professional, with a strong emphasis on the consultant role. The use of bold typography and contrasting colors creates a visually striking impact. The upward-facing graph and lines add a dynamic element, suggesting growth and progress. However, consider exploring different layouts or graphic elements to further enhance the design's uniqueness and appeal. "
        }}
        }}

                        
        input: {command}
        output:
        """

    

    response = model.generate_content(prompt_parts)
    
    print(response.text.strip().strip('`'))
    # print(response.text)
    return response.text.strip().strip('`')

def process_interpreted_command(interpreted_command):

    try:
        print("function called")
        interpreted_command = interpreted_command.strip('`')
        if interpreted_command.startswith("json"):
            interpreted_command = interpreted_command[4:].strip()
        print(interpreted_command)
        command_data = json.loads(interpreted_command)
        
        action = command_data["action"]
        parameters = command_data["parameters"]

        if action == "image_input":
            response = parameters["response"]
            print("inside image input")
            with st.chat_message("A"):
                    placeholder = st.empty()
                    typed_message = ""
                    for char in response:
                        typed_message += char
                        placeholder.write(typed_message)
                        time.sleep(0.02)
            st.session_state.messages.append({"role": "A", "content": response})

        elif action == "judge_image":
            response = parameters["response"]
            writeAssistantResponse(response)
            uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                print("inside")
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image.', use_column_width=True)
                st.session_state.messages.append({"role": "user", "content": "Uploaded an image."})
                result = interpret_command_with_gpt(image)
                process_interpreted_command(result)
            # st.session_state.messages.append({"role": "A", "content": response})
            
        elif action == "general_chat":
            response = parameters["response"]
            with st.chat_message("A"):
                    placeholder = st.empty()
                    typed_message = ""
                    for char in response:
                        typed_message += char
                        placeholder.write(typed_message)
                        time.sleep(0.02)
            st.session_state.messages.append({"role": "A", "content": response})

    except (json.JSONDecodeError, KeyError) as e:
        return f"Error processing command: {e}"

def writeAssistantResponse(response):
        with st.chat_message("A"):
                placeholder = st.empty()
                typed_message = ""
                for char in response:
                    typed_message += char
                    placeholder.write(typed_message)
                    time.sleep(0.03)
                for i in range(1, 4):
                    placeholder.write(response + i * ".")
                    time.sleep(1)
        st.session_state.messages.append({"role": "A", "content": response})

