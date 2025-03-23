import streamlit as st
from PIL import Image
import time
import os
from server.image_engine import image_detection
from server.ai_engine import chat
from server.firestore_dump import chat_load

st.subheader("📐Geometry Solver")

# Dropdown for selecting the tutoring method
if "user_data" in st.session_state:
    username = st.session_state["user_data"]["username"]
    prompt = st.session_state["user_data"]["prompt"]
    mode = st.selectbox("Choose your tutoring method:", ["Image", "Text"])
    if mode == "Image":
        st.subheader("🖼️ Upload an Image & Ask a Question")
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
        image_question = st.text_area("Question.. Ask away!!!")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            if st.button("Get Answer"):
                if image_question.strip():
                    response = image_detection(image_question, uploaded_file, username, prompt)                    
                    st.success(f"Your Answer is ready! 🎉")
                    st.markdown(response)
                    chat_load(st.session_state['user_data']['username'], "user", 'Image attached'+image_question)
                    chat_load(st.session_state['user_data']['username'], "model", response)
                else:
                    st.error("⚠️ Please enter a question about the image.")
    elif mode == "Text":
        st.subheader("📝 Enter Your Question")
        user_query = st.text_area("Question.. Ask away!!!")
        if st.button("Get Answer"):
            if user_query.strip():
                st.info("🔍 AI is processing your question... Please wait.")
                time.sleep(2)
                st.success("Your Answer is ready! 🎉")
                response = chat(user_query, prompt)
                st.markdown(response)
                chat_load(st.session_state['user_data']['username'], "user", user_query)
                chat_load(st.session_state['user_data']['username'], "model", response)
            else:
                st.error("⚠️ Please enter a question.")
else:
    st.error("You need to authenticate first. Please login or sign up.")