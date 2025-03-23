import streamlit as st
from server.firestore_dump import chat_load
from server.translator_engine import translate

st.title("🌍 Language Translator")

if "user_data" in st.session_state:
    # List of languages
    languages = [
        "English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Russian", "Arabic", 
        "Portuguese", "Italian", "Dutch", "Hindi", "Bengali", "Turkish", "Vietnamese", "Thai", "Swedish",
        "Greek", "Hebrew", "Polish", "Romanian", "Hungarian", "Czech", "Finnish", "Danish", "Norwegian"
    ]

    # Sidebar for language selection
    st.sidebar.header("Settings")
    source_lang = st.sidebar.selectbox("Translate from:", languages, index=languages.index("English"))
    target_lang = st.sidebar.selectbox("Translate to:", languages, index=languages.index("French"))
    input_method = st.sidebar.selectbox("Choose Input Method:", ["Text", "Voice"])

    # Layout for input and output
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Text" if input_method == "Text" else "Voice Input")
        if input_method == "Text":
            input_text = st.text_area("Enter text to translate:", height=200)
            response = translate(input_text, source_lang, target_lang)
        else:
            st.info("🎤 Voice input feature coming soon.")
    with col2:
        st.subheader("Translated Text")
        st.markdown(response)

    st.sidebar.info("Select languages from the dropdown and enter text or use voice input.")

else:
    st.error("You need to authenticate first. Please login or sign up.")