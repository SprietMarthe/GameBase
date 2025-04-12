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
                json.loads(firebase_key)
                print("Valid JSON format!")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
            try:
                # Parse the JSON string and initialize Firebase
                cred = credentials.Certificate(json.loads(firebase_key))
                firebase_admin.initialize_app(cred)
                st.success("Firebase initialized successfully.")
            except Exception as e:
                st.error(f"Error initializing Firebase: {e}")
                st.stop()
        else:
            st.error("Firebase credentials not found in Streamlit secrets.")
    
    return firebase_admin.get_app()

# Get Firestore database instance
def get_firestore_db():
    """Get Firestore database instance"""
    app = get_firebase_app()
    return firestore.client(app)
