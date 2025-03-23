import os
import json
from datetime import datetime
import google.generativeai as genai
import streamlit as st
from server.firestore_dump import chat_load

api_path = st.secrets["genai"]['api_key']

now = datetime.now()
dt_string = str(now.strftime("%d_%m_%Y"))
genai.configure(api_key=api_path)  
generation_config = {"temperature": 2}


safety = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def chat(user_input, initial_message):
    user_data = st.session_state["user_data"]
    username = user_data["username"]
    log_file = (f"logs/ai_logs/{username}/logconv_{dt_string}.json")
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
        chat_load(user_data['username'], "model", "Hiiiii, Shaun! What's up?! 😁")
    messages.append({"role": "user", "parts": user_input})
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05', system_instruction=initial_message, generation_config=generation_config, safety_settings=safety)
    chat_session = model.start_chat(history=messages)
    response = chat_session.send_message(str(user_input))
    response.resolve()
    response_content = response.text
    if response_content:
        messages.append({"role": "model", "parts": response_content})
        try:
            with open(log_file, 'w') as f:
                json.dump(messages, f, indent=4)
        except FileNotFoundError:
            os.makedirs(f"logs/ai_logs/{username}")
            with open(log_file, 'w') as f:
                json.dump(messages, f, indent=4)      
        return response_content
    else:
        return "You are left on READ... Sorry... Please wait a little longer for a reply..."