import streamlit as st

def check_login():
    """Check if the user is logged in as the developer."""
    correct_username = st.secrets["credentials"]["username"]
    correct_password = st.secrets["credentials"]["password"]

    # Check if already logged in, if yes, return True directly
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return True
    
    # Create placeholders for the login inputs and button
    username_placeholder = st.empty()
    password_placeholder = st.empty()
    button_placeholder = st.empty()

    # Username and password inputs
    username = username_placeholder.text_input("Username", "")
    password = password_placeholder.text_input("Password", "", type="password")

    # Login button
    login_button = button_placeholder.button("Login")

    # If button is clicked, check credentials
    if login_button:
        if username == correct_username and password == correct_password:
            st.session_state["logged_in"] = True  # Set logged in status
            st.session_state["username"] = username
            # st.success("You are logged in!")

            # Hide login form after successful login
            username_placeholder.empty()
            password_placeholder.empty()
            button_placeholder.empty()
            
            return True  # Return True for successful login
        else:
            st.session_state["logged_in"] = False  # Failed login
            st.error("Invalid username or password. Please try again.")
            return False  # Return False for failed login

    return False  # Default to False if login is not attempted