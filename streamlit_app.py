import streamlit as st
from login import check_login  # Import the login function
from pages.view_games import view_games  # Import view games page
from pages.settings import settings  # Import settings page (for adding/updating games)
from pages.about import about  # Import about page
from utils.helpers import custom_header
from firebase_config import get_firestore_db
from datetime import datetime, timezone
import uuid
from google.cloud.firestore_v1 import FieldFilter



# Page configuration
st.set_page_config(page_title="GameBase", page_icon="🎮", layout="wide")

def log_anonymous_visit():
    db = get_firestore_db()
    session_id = st.session_state.get("anonymous_id", "unknown")

    # Today’s date in ISO (YYYY-MM-DD)
    today_str = datetime.now(timezone.utc).date().isoformat()

    # Query for existing log for this session on this day
    existing_logs = db.collection("visit_logs") \
        .where(filter=FieldFilter("session_id", "==", session_id)) \
        .where(filter=FieldFilter("date", "==", today_str)) \
        .limit(1) \
        .stream()

    if not any(existing_logs):
        db.collection("visit_logs").add({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "date": today_str,
            "username": st.session_state.get("username", "anonymous"),
            "is_admin": st.session_state.get("admin_user_rights", False)
        })

if "anonymous_id" not in st.session_state:
    st.session_state["anonymous_id"] = str(uuid.uuid4())

log_anonymous_visit()


# Initialize the session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "View Games"

# Create two columns: one for the title and the other for the "More" dropdown
col1, col2 = st.columns([3, 1])

# Left column for the title
with col1:
    custom_header("GameBase")

# Right column for the "More" dropdown
with col2:
    # Use the session state to remember the current page
    menu = st.selectbox(
        "More", 
        options=["View Games", "Settings", "About"], 
        index=["View Games", "Settings", "About"].index(st.session_state.current_page),
        key="more_menu"
    )
    
    # Update the current page in session state when changed
    if menu != st.session_state.current_page:
        st.session_state.current_page = menu
        # Don't use st.rerun() here as it would create an infinite loop

# Handle navigation based on the selected menu
if menu == "Settings":
    settings()  # Call the settings page logic

elif menu == "About":
    about()  # Call the about page logic

elif menu == "View Games":
    view_games()  # Call the view games page logic