import json
import google.generativeai as genai
import PIL.Image
import streamlit as st
from datetime import datetime

def image_detection(caption, filename, username, initial_message):
    now = datetime.now()
    dt_string = str(now.strftime("%d_%m_%Y"))
    log_file = (f"logs/ai_logs/{username}/logconv_{dt_string}.json")
    try:
        with open(log_file, 'r') as f:
            messages = json.load(f)
    except FileNotFoundError:
        messages = []
    generation_config = {"temperature": 1.5}
    try:
        img = PIL.Image.open(filename)
        model = genai.GenerativeModel('gemini-2.0-pro-exp-02-05', system_instruction=initial_message, generation_config=generation_config)
        response = model.generate_content([caption, img], stream=True)
        response.resolve()
        try:
            summary = response.text
            messages.append({"role": "user", "parts": '$image' + caption})
            messages.append({"role": "model", "parts": summary})
            with open(log_file, 'w') as f:
                json.dump(messages, f, indent=4)
        except (KeyError, IndexError) as e:
            st.error(f"Error extracting text: {e}")
        return summary
    except Exception as e:
        st.error(f"Error summarizing image with Gemini: {e}")
        return None
