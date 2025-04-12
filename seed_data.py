"""
Script to seed the Firebase database with sample game data.
Run this once to populate your database.
"""

from firebase_config import get_firestore_db
import streamlit as st

# Sample games data
SAMPLE_GAMES = [
    {
    "game_name": "Pictionary",
    "game_type": "Drawing",
    "game_explanation": "Draw pictures to help your team guess a word or phrase within the time limit.",
    "difficulty": "Medium",
    "materials": ["Paper", "Pencils", "Timer", "Word cards"],
    "min_players": 4,
    "max_players": 10,
    "min_age": 8,
    "min_duration": 20,
    "max_duration": 40,
    "example": "One player draws a cat without speaking, while teammates try to guess 'cat' before time runs out.",
    "rules": "1. Divide into teams. 2. One player draws without speaking or gesturing. 3. Their team must guess the word before time runs out. 4. No letters or numbers allowed in drawings.",
    "score_calculation": "One point per correct guess. First team to reach 20 points wins.",
    "image_path": "",
    "expansions": ["Pictionary Ultimate Edition", "Pictionary Junior"],
    "drinking_rules": "When a team fails to guess correctly, each team member takes a sip."
}
]

def seed_database():
    """Seed the Firebase database with sample games data"""
    try:
        db = get_firestore_db()
        games_ref = db.collection("games")
        
        # Check if collection already has data
        existing_games = list(games_ref.limit(1).stream())
        if existing_games:
            st.warning("Your database already contains game data. Skipping seeding to avoid duplicates.")
            return False
        
        # Add sample games
        for game in SAMPLE_GAMES:
            games_ref.add(game)
        
        st.success(f"Successfully added {len(SAMPLE_GAMES)} sample games to the database.")
        return True
    except Exception as e:
        st.error(f"Error seeding database: {e}")
        return False

if __name__ == "__main__":
    st.set_page_config(page_title="Seed Games Database", page_icon="🎮")
    st.title("🎮 Seed Games Database")
    
    st.write("""
    This utility will add sample game data to your Firebase database.
    Only run this once to initialize your database with sample data.
    """)
    
    if st.button("Seed Database with Sample Games"):
        with st.spinner("Adding sample games..."):
            success = seed_database()
        
        if success:
            st.balloons()