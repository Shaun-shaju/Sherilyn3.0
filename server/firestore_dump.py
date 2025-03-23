from google.cloud import firestore
from datetime import datetime
import os

# Firestore Initialization
def initialize_firestore():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ("logs/firebase_auth.json")
    db = firestore.Client()
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
        return f"Error: {e}"
