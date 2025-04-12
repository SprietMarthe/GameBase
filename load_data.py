import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
from firebase_config import get_firestore_db

def load_games():
    """Fetch games from Firestore or fallback to CSV if Firebase is unavailable."""
    try:
        # Try to connect to Firestore and fetch the games
        db = get_firestore_db()
        games_ref = db.collection("games")
        games_docs = games_ref.stream()
        
        games = []
        for doc in games_docs:
            game_data = doc.to_dict()
            game_data['id'] = doc.id  # Add the document ID as a field
            games.append(game_data)
        
        # If Firebase is successful
        st.session_state['firebase_initialized'] = True
        return games
    except Exception as e:
        # If Firebase fails, show the fallback message and load demo games
        st.session_state['firebase_initialized'] = False
        st.error(f"Error loading games from Firebase: {e}")
        st.info("Falling back to CSV demo data...")
        return load_demo_games()

def load_demo_games():
    """Load demo games from a CSV file"""
    try:
        # Replace this with your actual CSV file path or data.
        demo_data = [
            {"game_name": "Uno", "game_type": "Card", "difficulty": "Easy", "number_of_players": "2-10", "age_range": "6+", "duration": "30 min", "materials": "UNO cards", "game_explanation": "Match cards by color or number"},
            {"game_name": "Monopoly", "game_type": "Board", "difficulty": "Medium", "number_of_players": "2-6", "age_range": "8+", "duration": "60 min", "materials": "Monopoly board, dice, cards", "game_explanation": "Collect properties and bankrupt your opponents"},
            {"game_name": "Chess", "game_type": "Board", "difficulty": "Hard", "number_of_players": "2", "age_range": "6+", "duration": "20-60 min", "materials": "Chess board, pieces", "game_explanation": "Strategic game of checkmate"},
        ]
        return demo_data
    except Exception as e:
        st.error(f"Error loading demo games from CSV: {e}")
        return []
