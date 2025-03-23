import streamlit as st
from google.cloud import firestore
import os
import bcrypt
import base64

# Firestore Initialization
def initialize_firestore():
    firestore_secrets = st.secrets["firestore"]  # Load credentials from Streamlit secrets
    db = firestore.Client.from_service_account_info(dict(firestore_secrets))  # Use the secrets
    return db

db = initialize_firestore()

# 🔹 Hashing Passwords for Security
def hash_password(password):
    """Hashes the password using bcrypt and encodes it for Firestore storage."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return base64.b64encode(hashed).decode()  # Convert binary to text-safe format

def check_password(password, hashed_password):
    """Verifies a password against its hashed version."""
    hashed_password = base64.b64decode(hashed_password.encode())  # Convert back to binary
    return bcrypt.checkpw(password.encode(), hashed_password)

# 🔹 User Authentication
st.subheader("🔒 Profile Settings")
username = st.text_input("Enter your Username")
password = st.text_input("Enter Password", type="password")
flag = False
if st.button("Login"):
    doc = db.collection("users").document(username).get()
    if doc.exists:
        data = doc.to_dict()
        if check_password(password, data["password"]):  
            flag = True
        else:
            st.error("Invalid login credentials. ❌")
    else:
        st.error("User not found. Please sign up first.")

# 🔹 Display and Edit Profile Fields
if flag:
    user_info = st.session_state['user_data']
    
    name = st.text_input("Name", value=user_info.get("name"))
    age = st.number_input("Age", min_value=15, max_value=120, value=user_info.get("age"))
    personality = st.text_input("Personality Type", value=user_info.get("personality"))
    style = st.text_input("Chat Style", value=user_info.get("style"))
    topics = st.text_input("Topics of Discussion", value=user_info.get("topics"))
    behaviour = st.text_input("Expected Behaviour", value=user_info.get("behaviour"))

    # 🔹 Change Password Section
    st.subheader("🔑 Change Password")
    old_password = st.text_input("Enter Current Password", type="password")
    new_password = st.text_input("Enter New Password", type="password")
    confirm_new_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if check_password(old_password, st.session_state['user_data']["password"]):  # Check hashed password
            if new_password == confirm_new_password:
                db.collection("users").document(username).update({"password": hash_password(new_password)})
                st.success("✅ Password updated successfully!")
            else:
                st.error("❌ New passwords do not match.")
        else:
            st.error("❌ Incorrect current password.")

    # 🔹 Save Profile Changes
    if st.button("Save Changes"):
        updated_info = {
            "name": name,
            "age": age,
            "personality": personality,
            "style": style,
            "topics": topics,
            "behaviour": behaviour,
        }
        db.collection("users").document(username).update(updated_info)
        st.success("✅ Profile updated successfully!")
else:
    st.error("You need to authenticate first. Please login or sign up.")