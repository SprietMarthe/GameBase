import streamlit as st
import bcrypt
from firebase_config import get_firestore_db

def add_user():
    st.subheader("Add New User")

    with st.form("add_user_form"):
        username = st.text_input("Username*", help="Must be unique").lower()
        password = st.text_input("Password*", type="password", help="Choose a strong password")
        is_admin = st.checkbox("Give admin user rights")
        submit = st.form_submit_button("Add User")

        if submit:
            if not username or not password:
                st.error("Both username and password are required.")
                return

            db = get_firestore_db()
            users_ref = db.collection("users")

            # Check if user already exists
            existing = list(users_ref.where("username", "==", username).limit(1).stream())
            if existing:
                st.error("Username already exists.")
                return

            try:
                # Hash the password
                hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                # Add user
                users_ref.add({
                    "username": username,
                    "password_hash": hashed_pw,
                    "admin_user_rights": is_admin
                })

                st.success(f"User '{username}' added successfully!")
            except Exception as e:
                st.error(f"Error adding user: {e}")
