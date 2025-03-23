import streamlit as st
from PIL import Image
import time
import os
from server.image_engine import image_detection
from server.ai_engine import chat as recipe_en
from server.firestore_dump import chat_load

st.subheader("🍲 Recipe Maker")

# Function to create a recipe
if "user_data" in st.session_state:
    username = st.session_state["user_data"]["username"]
    # Dropdown menu for selecting options
    option = st.selectbox("Select your search method", 
                          ["Search by Image", "Search by Dish Name", "Find Dishes by Ingredients"])

    if option == "Search by Image":
        prompt = st.session_state["user_data"]["prompt"] + "Identify the dish from the image and create a detailed recipe for a dish using the following parameters: the dish should be [Dish Type] with [Main Ingredients], and it should be [Cuisine]. The cooking method should be [Cooking Method]. Please provide the recipe in the following format: Dish Name, Preparation Time, Cooking Time, followed by a list of ingredients with exact measurements. Include step-by-step instructions for preparation and cooking, and finish with serving suggestions. Additionally, provide any helpful tips for the dish, such as variations or storage suggestions. Make sure the recipe is clear, easy to follow, and tailored to the dish type, ingredients, and cooking method provided. Let the recipe follow user's choice of personality, style, topics, and behaviour."
        st.subheader("Search for a recipe by image")
        # Placeholder for image recognition mechanism
        uploaded_image = st.file_uploader("Gimme the dish.. Ill give you the recipe 😍", type=["jpg", "png", "jpeg"])
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            image_question = st.text_area("Add query to the image.. (Optional)")
            if image_question == "":
                image_question = ": Identify the dish for me plz"
            if st.button("Get Answer"):
                if image_question.strip():
                    st.info(f"Lemme look at it.. Gimme a moment 😒😒")
                    response = image_detection(image_question, uploaded_image, username, prompt)                    
                    st.success(f"Your Answer is ready! 🎉")
                    st.markdown(response)
                    chat_load(st.session_state['user_data']['username'], "user", 'Image attached' + image_question)
                    chat_load(st.session_state['user_data']['username'], "model", response)
                else:
                    st.error("⚠️ Please enter a question about the image.")

    elif option == "Search by Dish Name":
        st.subheader("Search for a recipe by dish name")
        dish_name = st.text_input("Enter the name of the dish:")
        prompt = st.session_state['user_data']['prompt'] + "Create a detailed recipe for a dish using the following parameters: the dish should be [Dish Type] with [Main Ingredients], and it should be [Cuisine]. The cooking method should be [Cooking Method]. Please provide the recipe in the following format: Dish Name, Preparation Time, Cooking Time, followed by a list of ingredients with exact measurements. Include step-by-step instructions for preparation and cooking, and finish with serving suggestions. Additionally, provide any helpful tips for the dish, such as variations or storage suggestions. Make sure the recipe is clear, easy to follow, and tailored to the dish type, ingredients, and cooking method provided. Let the recipe follow user's choice of personality, style, topics, and behaviour."
        if dish_name:            
            st.info(f"Lemme look at it.. Gimme a moment 😒😒")
            response = recipe_en(dish_name, prompt)
            st.success(f"Your Answer is ready! 🎉")
            st.markdown(response)
            chat_load(st.session_state['user_data']['username'], "user", "recipe_maker: " + dish_name)
            chat_load(st.session_state['user_data']["username"], "model", response)

    elif option == "Find Dishes by Ingredients":
        st.subheader("Find dishes based on ingredients")
        ingredients = st.text_area("Gimme what you got. Ill tell you what you can make with them 😉.")
        prompt = st.session_state['user_data']['prompt'] + "Create a detailed recipe for a dish using the following parameters: the dish should be [Dish Type] with [Main Ingredients], and it should be [Cuisine]. The cooking method should be [Cooking Method]. Please provide the recipe in the following format: Dish Name, Preparation Time, Cooking Time, followed by a list of ingredients with exact measurements. Include step-by-step instructions for preparation and cooking, and finish with serving suggestions. Additionally, provide any helpful tips for the dish, such as variations or storage suggestions. Make sure the recipe is clear, easy to follow, and tailored to the dish type, ingredients, and cooking method provided. Let the recipe follow user's choice of personality, style, topics, and behaviour."
        if ingredients:
            st.info(f"Lemme look at it.. Gimme a moment 😒😒")
            response = recipe_en(ingredients, prompt)
            st.success(f"Your Answer is ready! 🎉")
            st.markdown(response)
            chat_load(st.session_state['user_data']['username'], "user", "recipe_maker: " + ingredients)
            chat_load(st.session_state['user_data']['username'], "model", response)
else:
    st.error("You need to authenticate first. Please login or sign up.")