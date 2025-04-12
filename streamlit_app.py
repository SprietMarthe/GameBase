import streamlit as st
from login import check_login  # Import the login function
from pages.view_games import view_games  # Import view games page
from pages.settings import settings  # Import settings page (for adding/updating games)
from pages.about import about  # Import about page
from utils.helpers import custom_header

# Page configuration
st.set_page_config(page_title="GameBase", page_icon="🎮", layout="wide")

# Create two columns: one for the title and the other for the "More" dropdown
col1, col2 = st.columns([3, 1])

# Left column for the title
with col1:
    custom_header("GameBase")

# Right column for the "More" dropdown
with col2:
    menu = st.selectbox("More", options=["View Games", "Settings", "About"], key="more_menu")

# Handle the "Log In" menu option
if menu == "Settings":
    settings()  # Call the settings page logic

elif menu == "About":
    about()  # Call the about page logic

elif menu == "View Games":
    view_games()  # Call the view games page logic
