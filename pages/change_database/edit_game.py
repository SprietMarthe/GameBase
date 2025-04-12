import streamlit as st

from load_data import load_games

def edit_game():
    """Form to edit an existing game"""
    st.subheader("Edit an Existing Game")
    
    # Load games to select which one to edit
    games = load_games()
    game_names = [game['game_name'] for game in games]
    selected_game = st.selectbox("Select Game to Edit", game_names)

    if selected_game:
        # Get the selected game data
        game = next(game for game in games if game['game_name'] == selected_game)

        # Display form with pre-filled data for editing
        with st.form("edit_game_form"):
            new_game_name = st.text_input("Game Name", game['game_name'])
            new_game_type = st.text_input("Game Type", game['game_type'])
            new_difficulty = st.text_input("Difficulty", game['difficulty'])
            new_number_of_players = st.text_input("Number of Players", game['number_of_players'])
            new_age_range = st.text_input("Age Range", game['age_range'])
            new_duration = st.text_input("Duration", game['duration'])
            new_materials = st.text_input("Materials", game['materials'])
            new_game_explanation = st.text_area("Game Explanation", game['game_explanation'])

            submitted = st.form_submit_button("Save Changes")
            if submitted:
                st.success("Game updated successfully!")
                # Add code to update the game in Firebase or CSV