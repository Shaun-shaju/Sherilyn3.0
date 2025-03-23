import os
import json
from datetime import datetime
import google.generativeai as genai
import streamlit as st

now = datetime.now()
dt_string = str(now.strftime("%d_%m_%Y"))
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

def translate(user_input, source, target):
    prompt = f"You are a language translator. You will translate the given sentence from {source} to {target}"
    user_data = st.session_state["user_data"]
    username = user_data["username"]
    messages = []
    messages.append({"role": "user", "parts": user_input})
    model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05', system_instruction=prompt, generation_config=generation_config, safety_settings=safety)
    chat_session = model.start_chat(history=messages)
    response = chat_session.send_message(str(user_input))
    response.resolve()
    response_content = response.text
    if response_content:
        messages.append({"role": "model", "parts": response_content})    
        return response_content
    else:
        return "You are left on READ... Sorry... Please wait a little longer for a reply..."