from google.cloud import firestore
from datetime import datetime
import os
import streamlit as st

# Firestore Initialization
def initialize_firestore():
    firestore_secrets = st.secrets["firestore"]  # Load credentials from Streamlit secrets
    db = firestore.Client.from_service_account_info(dict(firestore_secrets))  # Use the secrets
    return db

db = initialize_firestore()

def chat_load(username, role, text):
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y")

    try:
        # Reference to user's chat collection for the day
        user_ref = db.collection("chat_data").document(username).collection(dt_string)
        
        # Get the count of messages efficiently
        message_count = len(list(user_ref.list_documents())) + 1  # Increment for new message

        chat_data = {
            "role": role,
            "parts": str(text),
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        
        # Store each message in a new document
        user_ref.document(str(message_count)).set(chat_data)

    except Exception as e:
        return f"Firestore Error: {e}"
