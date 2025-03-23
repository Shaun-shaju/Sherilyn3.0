import streamlit as st
from google.cloud import firestore
import json
import bcrypt
import base64  # To properly encode and decode passwords

# Firestore Initialization using Streamlit Secrets
def initialize_firestore():
    firestore_secrets = st.secrets["firestore"]  # Load credentials from Streamlit secrets
    db = firestore.Client.from_service_account_info(dict(firestore_secrets))  # Use the secrets
    return db

db = initialize_firestore()

def hash_password(password):
    """Hashes the password using bcrypt and encodes it for Firestore storage."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return base64.b64encode(hashed).decode()  # Convert binary to text-safe format

def check_password(password, hashed_password):
    """Verifies a password against its hashed version."""
    hashed_password = base64.b64decode(hashed_password.encode())  # Convert back to binary
    return bcrypt.checkpw(password.encode(), hashed_password)

def prompt_engines(lt):
    name = lt[2]
    age = lt[3]
    personality = lt[4]
    style = lt[5]
    topics = lt[6]
    behaviour = lt[7]
    prompt = f"You are Sherilyn. Most Advanced AI system made by S. Shaun Benedict. You are to behave like a girl same as the user's age. You're free to use nicknames or just the first name. Dont use the full name. The User's Name is {name}, Age is {age}. Your Personality is {personality}, Style of chat will be {style}, Topics you discuss will be {topics}, Your Behaviour will be {behaviour}."
    return prompt

def signup():
    """Handles user signup and securely stores hashed passwords in Firestore."""
    st.subheader("Create an Account")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")
    rep_password = st.text_input("Re-enter Password", type="password")

    if password != rep_password:
        st.error("Passwords do not match. Please try again.")
        return None

    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age", min_value=15, max_value=120)
    personality = st.text_input("Personality Type")
    style = st.text_input("Chat Style")
    topics = st.text_input("Topics of Discussion")
    behaviour = st.text_input("Expected Behaviour")

    if st.button("Sign Up"):
        hashed_password = hash_password(password)  # Hash password correctly
        user_data = {
            "username": username,
            "password": hashed_password,  # Now safely stored
            "name": name,
            "age": age,
            "personality": personality,
            "style": style,
            "topics": topics,
            "behaviour": behaviour,
            "prompt": prompt_engines([username, password, name, age, personality, style, topics, behaviour]),
        }
        try:
            db.collection("users").document(username).set(user_data)
            st.success(f"User '{username}' created successfully! Please log in.")
            return True
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    return None

def login():
    """Handles user login by verifying hashed passwords."""
    st.subheader("Login to your Account")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        doc = db.collection("users").document(username).get()
        if doc.exists:
            data = doc.to_dict()
            if check_password(password, data["password"]):  # Verify hashed password
                st.success(f"Welcome, {data['name']}! 🎉")
                return data
            else:
                st.error("Invalid login credentials. ❌")
        else:
            st.error("User not found. Please sign up first.")
    return None