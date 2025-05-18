import streamlit as st
import bcrypt
from firebase_config import get_firestore_db
from google.cloud.firestore_v1 import FieldFilter
from datetime import datetime, timezone
datetime.now(timezone.utc).isoformat()


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
    username = username_placeholder.text_input("Username", "").lower()
    password = password_placeholder.text_input("Password", "", type="password")
    login_button = button_placeholder.button("Login")

    if login_button:
        try:
            docs = users_ref.where(filter=FieldFilter("username", "==", username)).limit(1).stream()
            user_doc = next(docs, None)

            if not user_doc:
                log_login_attempt(username, success=False)
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

                log_login_attempt(username, success=True)
                update_visit_log_after_login()

                return True
            else:
                log_login_attempt(username, success=False)
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"Login failed: {e}")

    return False



def log_login_attempt(username, success):
    try:
        db = get_firestore_db()
        session_id = st.session_state.get("anonymous_id", "unknown")
        today_str = datetime.now(timezone.utc).date().isoformat()

        attempts_ref = db.collection("login_attempts")

        # Look for existing attempt for this session today
        existing_logs = attempts_ref \
            .where(filter=FieldFilter("session_id", "==", session_id)) \
            .where(filter=FieldFilter("date", "==", today_str)) \
            .limit(1) \
            .stream()

        for doc in existing_logs:
            doc.reference.update({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "username": username,
                "success": success,
                "tries": doc.to_dict().get("tries", 1) + 1
            })
            return

        # If not found, create new log entry
        attempts_ref.add({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "username": username,
            "success": success,
            "session_id": session_id,
            "date": today_str,
            "tries": 1
        })

    except Exception as e:
        st.warning(f"Could not log login attempt: {e}")




def update_visit_log_after_login():
    db = get_firestore_db()
    session_id = st.session_state.get("anonymous_id", "unknown")
    today_str = datetime.now(timezone.utc).date().isoformat()

    logs = db.collection("visit_logs") \
        .where(filter=FieldFilter("session_id", "==", session_id)) \
        .where(filter=FieldFilter("date", "==", today_str)) \
        .limit(1) \
        .stream()

    for doc in logs:
        doc.reference.update({
            "username": st.session_state.get("username", "unknown"),
            "is_admin": st.session_state.get("admin_user_rights", False)
        })
        break  # Only update the first match