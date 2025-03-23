import streamlit as st
import time
import sys
sys.path.append("pages")  # Add 'pages' to the module search path
from pages.auth import login, signup

st.title("Sherilyn AI")
# st.markdown(
#     """
#     <style>
#         /* Hide "Deploy" button */
#         [data-testid="stToolbar"] { visibility: hidden !important; }

#         /* Hide the top-right menu */
#         header { visibility: hidden; }

#         /* Hide Streamlit branding */
#         footer { visibility: hidden; }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
def authenticate():
    st.title("🌟 Welcome to Sherilyn AI 🌟")
    
    with st.spinner("Loading AI magic... ✨"):
        time.sleep(2)  # Simulate a loading effect
    
    st.success("Welcome to the future of AI! 🤖💡")
    
    st.markdown("""
        **Sherilyn AI** is an advanced personal AI assistant designed by **S. Shaun Benedict**.
        
        - 🤖 **Chat with an intelligent AI**  
        - 🔒 **Secure login system**  
        - 🎨 **Customizable AI personalities**  
        
        🚀 *Let's get started!*
    """)
    
    # Buttons for navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", key="login_btn"):
            st.session_state.page = "login"
            st.rerun()
    
    with col2:
        if st.button("📝 Sign Up", key="signup_btn"):
            st.session_state.page = "signup"
            st.rerun()

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Check which page to show
if "page" not in st.session_state:
    st.session_state.page = "welcome"

elif st.session_state.page == "login":
    st.subheader("🔑 Login to Your Account")
    data = login()
    if data:
        st.session_state["authenticated"] = True
        st.session_state["user_data"] = data
        st.session_state.page = "dashboard"  # Redirect after login
        st.rerun()
elif st.session_state.page == "signup":
    st.subheader("📝 Create a New Account")
    data = signup()
    if data:
        st.session_state["authenticated"] = True
        st.session_state.page = "dashboard"  # Redirect after signup
        st.rerun()
elif st.session_state.page == "dashboard":
    st.subheader(f"Welcome, {st.session_state['user_data']['name']}! 🎉")
    st.write("You're now logged in! 🚀")
    if st.button("🚪 Logout", key="dashboard_logout"):
        st.session_state["authenticated"] = False
        st.session_state.page = "welcome"
        st.rerun()

def logout():
    st.session_state["authenticated"] = False
    st.session_state.page = "welcome"

pages = {
    "Account": [
        st.Page(authenticate, title="Dashboard", icon="🏠"),
        st.Page("pages/profile.py", title="Profile Settings", icon="🔒"),
    ],
    "Apps": [
        st.Page("pages/chat_screen.py", title="Chat with Sherilyn", icon="🤖"),
        st.Page("pages/tutor.py", title="Personal Tutor", icon="📚"),
        st.Page("pages/recipe.py", title="Recipe Maker", icon="🍲"),
        st.Page("pages/geometry.py", title="Geometry Solver", icon="📐"),
        st.Page("pages/trip_planner.py", title="Travel Planner", icon = "🌍"),
        # st.Page("pages/translator.py", title="Language Translator", icon = "🌐"),
        st.Page("pages/weather.py", title="Weather Forecast", icon="🌦️"),
        # st.Page("pages/news.py", title="Latest News", icon="📰"),
        st.Page("pages/help.py", title="Get Help", icon="🆘"),
        st.Page("pages/about.py", title="About the Developer", icon="👨‍💻"),
    ],
}

pg = st.navigation(pages)
if st.session_state.get("authenticated", False):
    st.sidebar.button("🚪 Logout", key="sidebar_logout", on_click=logout)  # Unique key added
pg.run()
