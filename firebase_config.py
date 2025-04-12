import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os

# Setup Firebase connection
@st.cache_resource
def get_firebase_app():
    """Initialize Firebase app with caching to avoid multiple initializations"""
    
    # Check if the app is already initialized
    if not firebase_admin._apps:
        # Look for the Firebase key JSON file
        if os.path.exists("firebase-key-gamebase.json"):
            try:
                cred = credentials.Certificate("firebase-key-gamebase.json")
                firebase_admin.initialize_app(cred)
            except Exception as e:
                st.error(f"Error initializing Firebase: {e}")
                st.stop()
        else:
            st.error("Firebase credentials not found. Please add firebase-key-gamebase.json file to your project.")
            st.stop()
    
    return firebase_admin.get_app()

# Get Firestore database instance
def get_firestore_db():
    """Get Firestore database instance"""
    app = get_firebase_app()
    return firestore.client(app)