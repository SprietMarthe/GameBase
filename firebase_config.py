import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Setup Firebase connection using Streamlit secrets
@st.cache_resource
def get_firebase_app():
    """Initialize Firebase app with caching to avoid multiple initializations"""
    
    # Check if the app is already initialized
    if not firebase_admin._apps:
        # Get Firebase credentials from Streamlit secrets
        firebase_key = st.secrets["firebase"]["FIREBASE_KEY"]

        if firebase_key:
            try:
                # Load the Firebase credentials from the string stored in secrets.toml
                cred = credentials.Certificate(json.loads(firebase_key))  # Parse the JSON string
                firebase_admin.initialize_app(cred)
            except Exception as e:
                st.error(f"Error initializing Firebase: {e}")
                st.stop()
        else:
            st.error("Firebase credentials not found in Streamlit secrets. Please set FIREBASE_KEY.")
            st.stop()
    
    return firebase_admin.get_app()

# Get Firestore database instance
def get_firestore_db():
    """Get Firestore database instance"""
    app = get_firebase_app()
    return firestore.client(app)
