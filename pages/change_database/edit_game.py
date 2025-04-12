import streamlit as st
from load_data import load_games
from firebase_config import get_firestore_db

def edit_game():
    """Form to edit an existing game"""
    st.subheader("Edit an Existing Game")
    
    # Initialize session state variables for editing process
    if 'edit_game_selected' not in st.session_state:
        st.session_state.edit_game_selected = None
    
    if 'edit_status' not in st.session_state:
        st.session_state.edit_status = None
    
    # Load games to select which one to edit
    games = load_games()
    
    if not games:
        st.error("No games available to edit.")
        return
    
    # Extract game names for the dropdown
    game_names = [game.get('game_name', 'Unnamed Game') for game in games]
    
    # Game selection dropdown
    selected_game = st.selectbox(
        "Select Game to Edit", 
        options=game_names,
        index=0 if st.session_state.edit_game_selected is None else 
              game_names.index(st.session_state.edit_game_selected) 
              if st.session_state.edit_game_selected in game_names else 0,
        key="edit_game_selectbox"
    )
    
    # Update the selected game in session state
    st.session_state.edit_game_selected = selected_game
    
    if selected_game:
        # Get the selected game data
        game = next((game for game in games if game.get('game_name') == selected_game), None)
        
        if game:
            # Display form with pre-filled data for editing
            with st.form("edit_game_form"):
                st.subheader(f"Editing: {selected_game}")
                
                # Basic game information
                new_game_name = st.text_input("Game Name", game.get('game_name', ''))

                # Determine the current game type and if it's a custom "Other" type
                game_types_data = load_game_types()
                game_type_options = [gt['name'] for gt in game_types_data]
                current_type = game.get('game_type', '')
                is_other_type = not any(current_type == option for option in game_type_options)
                other_type_value = ""

                if is_other_type:
                    # Extract the custom type if it starts with "Other: "
                    if current_type.startswith("Other: "):
                        other_type_value = current_type[7:]  # Remove the "Other: " prefix
                    selected_index = game_type_options.index("Other")
                else:
                    # Find the index of the matching game type
                    selected_index = game_type_options.index(current_type) if current_type in game_type_options else 0

                # Display the game type dropdown
                new_game_type = st.selectbox("Game Type", 
                                        game_type_options,
                                        index=selected_index)

                # Show a text input if "Other" is selected
                if new_game_type == "Other":
                    other_type = st.text_input("Please specify game type", value=other_type_value)
                    if other_type:
                        new_game_type = f"Other: {other_type}"




                new_difficulty = st.selectbox("Difficulty", 
                                            ["Easy", "Medium", "Hard"],
                                            index=["Easy", "Medium", "Hard"].index(game.get('difficulty', 'Medium')) 
                                            if game.get('difficulty') in ["Easy", "Medium", "Hard"] else 1)
                
                # Player information
                col1, col2 = st.columns(2)
                with col1:
                    new_min_players = st.number_input("Min Players", 
                                                    min_value=1, 
                                                    value=game.get('min_players', 1))
                with col2:
                    new_max_players = st.number_input("Max Players", 
                                                    min_value=new_min_players, 
                                                    value=max(game.get('max_players', 4), new_min_players))
                
                # Age and duration
                col1, col2 = st.columns(2)
                with col1:
                    new_min_age = st.number_input("Minimum Age", 
                                                min_value=0, 
                                                value=game.get('min_age', 8))
                with col2:
                    new_min_duration = st.number_input("Duration (minutes)", 
                                                    min_value=1, 
                                                    value=game.get('min_duration', 30))
                
                # Materials (as a comma-separated string)
                materials_default = ', '.join(game.get('materials', [])) if isinstance(game.get('materials'), list) else game.get('materials', '')
                new_materials = st.text_area("Materials (comma separated)", materials_default)
                
                # Game details
                new_game_explanation = st.text_area("Game Explanation", game.get('game_explanation', ''))
                new_rules = st.text_area("Rules", game.get('rules', ''))
                new_score_calculation = st.text_area("Score Calculation", game.get('score_calculation', ''))
                new_example = st.text_area("Example", game.get('example', ''))
                
                # Optional fields
                expander = st.expander("Additional Options")
                with expander:
                    new_expansions = st.text_area("Expansions (comma separated)", 
                                                ', '.join(game.get('expansions', [])) if isinstance(game.get('expansions'), list) else game.get('expansions', ''))
                    new_drinking_rules = st.text_area("Drinking Rules (optional)", game.get('drinking_rules', ''))
                
                # Submit button
                submitted = st.form_submit_button("Save Changes")
                
                if submitted:
                    try:
                        # Prepare updated game data
                        updated_game = {
                            'game_name': new_game_name,
                            'game_type': new_game_type,
                            'difficulty': new_difficulty,
                            'min_players': new_min_players,
                            'max_players': new_max_players,
                            'min_age': new_min_age,
                            'min_duration': new_min_duration,
                            'materials': [item.strip() for item in new_materials.split(',') if item.strip()],
                            'game_explanation': new_game_explanation,
                            'rules': new_rules,
                            'score_calculation': new_score_calculation,
                            'example': new_example,
                            'expansions': [item.strip() for item in new_expansions.split(',') if item.strip()],
                            'drinking_rules': new_drinking_rules
                        }
                        
                        # Get Firestore database
                        db = get_firestore_db()
                        games_ref = db.collection("games")
                        
                        # Query for the game document
                        query = games_ref.where("game_name", "==", selected_game).limit(1).stream()
                        
                        # Find and update the document
                        doc_found = False
                        for doc in query:
                            doc.reference.update(updated_game)
                            doc_found = True
                            break
                        
                        if doc_found:
                            # Update status in session state
                            st.session_state.edit_status = "success"
                            st.session_state.edited_game_name = new_game_name
                        else:
                            st.session_state.edit_status = "error_not_found"
                        
                    except Exception as e:
                        st.session_state.edit_status = "error"
                        st.session_state.edit_error = str(e)
        else:
            st.error(f"Could not find data for game: {selected_game}")
    
    # Display status messages based on session state
    if st.session_state.edit_status == "success":
        st.success(f"'{st.session_state.edited_game_name}' has been updated successfully!")
        if st.button("Clear", key="clear_edit_success"):
            st.session_state.edit_status = None
            st.session_state.edited_game_name = None
            # Rerun to refresh the game list if name changed
            st.rerun()
    
    elif st.session_state.edit_status == "error_not_found":
        st.error(f"Game not found in database. It may have been deleted.")
        if st.button("Clear", key="clear_edit_error_not_found"):
            st.session_state.edit_status = None
    
    elif st.session_state.edit_status == "error":
        st.error(f"Error updating game: {st.session_state.edit_error}")
        if st.button("Clear", key="clear_edit_error"):
            st.session_state.edit_status = None
            st.session_state.edit_error = None