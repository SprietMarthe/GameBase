import streamlit as st

from load_data import load_games

def delete_game():
    """Form to delete a game"""
    st.subheader("Delete a Game")
    
    # Load games to select which one to delete
    games = load_games()
    game_names = [game['game_name'] for game in games]
    selected_game = st.selectbox("Select Game to Delete", game_names)

    if selected_game:
        if st.button(f"Delete {selected_game}"):
            # Add code to delete the game from Firebase or CSV
            st.success(f"{selected_game} deleted successfully!")