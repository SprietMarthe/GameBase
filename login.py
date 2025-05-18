import streamlit as st
import bcrypt
from firebase_config import get_firestore_db

def check_login():
    """Check if the user is logged in using Firestore + bcrypt, with UI placeholders."""

    db = get_firestore_db()
    users_ref = db.collection("users")

    # Return early if already logged in
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return True

    # Create UI placeholders
    username_placeholder = st.empty()
    password_placeholder = st.empty()
    button_placeholder = st.empty()

    # Inputs
    username = username_placeholder.text_input("Username", "")
    password = password_placeholder.text_input("Password", "", type="password")
    login_button = button_placeholder.button("Login")

    if login_button:
        try:
            docs = users_ref.where("username", "==", username).limit(1).stream()
            user_doc = next(docs, None)

            if not user_doc:
                st.error("Invalid username or password.")
                return False

            user = user_doc.to_dict()
            stored_hash = user["password_hash"].encode()

            if bcrypt.checkpw(password.encode(), stored_hash):
                # Login successful
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["admin_user_rights"] = user.get("admin_user_rights", False)

                # Clear placeholders
                username_placeholder.empty()
                password_placeholder.empty()
                button_placeholder.empty()

                return True
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Login failed: {e}")

    return False
