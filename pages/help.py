import streamlit as st

st.title("📌 Help Menu")

help_menu = {
    "Personal Tutor": {
        "Description": "Get assistance with your studies, including explanations, problem-solving, and personalized learning plans.",
        "Example": "Example: *Can you help me understand the Pythagorean theorem?*"
    },
    "Recipe Finder": {
        "Description": "Discover new recipes based on your preferences or available ingredients.",
        "Example": "Example: *Suggest a dinner recipe with chicken and broccoli.*"
    },
    "Geometry Solver": {
        "Description": "Solve geometry problems.",
        "Example": "Example: *How do I calculate the area of a trapezoid?*"
    },
    "Trip Planner": {
        "Description": "Get help planning trips, including destination suggestions, itineraries, and travel tips.",
        "Example": "Example: *Plan a 3-day trip to Paris with must-see attractions.*"
    },
    "Weather Forecast": {
        "Description": "Check the current weather and forecasts for your location or any city.",
        "Example": "Example: *What's the weather like in Bangalore today?*"
    },
    "Language Translator (Coming Soon)": {
        "Description": "Translate text between different languages.",
        "Example": "Example: *How do you say 'good morning' in Japanese?*"
    },
    "Music Recommendations(Coming Soon)": {
        "Description": "Receive music suggestions based on your mood or favorite genres.",
        "Example": "Example: *Recommend some upbeat pop songs.*"
    },
    "News Updates (Coming Soon)": {
        "Description": "Stay informed with the latest news in various categories.",
        "Example": "Example: *What's the latest in technology news?*"
    },
    "Fitness Tips (Coming Soon)": {
        "Description": "Receive workout routines and fitness advice.",
        "Example": "Example: *Suggest a beginner's workout plan.*"
    }
}

for feature, details in help_menu.items():
    with st.expander(f"🔹 {feature}"):
        st.write(f"📝 {details['Description']}")
        st.info(f"📌 {details['Example']}")
