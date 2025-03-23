import streamlit as st
import time
import json
import os
from datetime import datetime
from server import ai_engine  
from google.cloud import firestore

# Firestore Initialization
def initialize_firestore():
    firestore_secrets = st.secrets["firestore"]  # Load credentials from Streamlit secrets
    db = firestore.Client.from_service_account_info(dict(firestore_secrets))  # Use the secrets
    return db

db = initialize_firestore()

def chat_load(username, role, text):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y")
    
    # Get the total number of messages for this user & date
    user_ref = db.collection("chat_data").document(username).collection(dt_string)
    docs = user_ref.stream()
    
    message_count = sum(1 for _ in docs) + 1  # Incremental message number
    
    chat_data = {
        "role": role,
        "parts": str(text),
        "timestamp": firestore.SERVER_TIMESTAMP
    }
    
    try:
        user_ref.document(str(message_count)).set(chat_data)  # Store each message in a new document
    except Exception as e:
        st.error(f"Error: {e}")

def sync_chat_from_firestore(username):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y")
    log_file = (f"logs/ai_logs/{username}/logconv_{dt_string}.json")
    
    os.makedirs(f"logs/ai_logs/{username}", exist_ok=True)

    user_ref = db.collection("chat_data").document(username).collection(dt_string)
    docs = user_ref.stream()
    
    chat_history = [{"role": doc.to_dict()["role"], "parts": doc.to_dict()["parts"]} for doc in docs]

    try:
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=4)
    except Exception as e:
        st.error(f"Failed to save chat log: {e}")

    return chat_history
st.subheader("🤖 Chat with Sherilyn")
if "user_data" in st.session_state:
    user_data = st.session_state["user_data"]
    chat_history = sync_chat_from_firestore(user_data['username'])  # Load and save chat history

    prompt = user_data['prompt']
    
    st.write("Hey bestie! Chat with me anytime! 😊✨ Im sorry but my memory gets updated every day 😭😭😭")

    if "messages" not in st.session_state:
        st.session_state.messages = chat_history if chat_history else [{"role": "model", "parts": "Hiiiii, Shaun! What's up?! 😁"}]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["parts"])

    user_input = st.chat_input("Type your message...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "parts": user_input})
        chat_load(user_data['username'], "user", user_input)  # Store user input
        
        st.chat_message("user").write(user_input)

        with st.spinner("Thinking... 🤔"):
            time.sleep(1)
            response = ai_engine.chat(user_input, initial_message=prompt)

        st.session_state.messages.append({"role": "assistant", "parts": response})
        st.chat_message("assistant").write(response)
        chat_load(user_data['username'], "model", response)  # Store AI response

else:
    st.error("You need to authenticate first. Please login or sign up.")
