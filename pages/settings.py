import streamlit as st
from login import check_login  # Import the login function from login.py
from pages.change_database.database_manager import change_database


def settings():
    """Page for adding/updating games"""
    
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        # If not logged in, show the login page first
        if check_login():  # Check if the developer logs in
            st.session_state["logged_in"] = True  # Set session state to logged in
            st.success("You are logged in!")
            change_database()  # Redirect to the Add Game page
        else:
            st.warning("Please log in to add or update games.")
    else:
        # If logged in, go directly to the Add Game page
        change_database()
