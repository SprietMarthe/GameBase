import streamlit as st
from firebase_config import get_firestore_db
from game_types import load_game_types

def add_game():
    """Form for adding a new game to the database"""
    st.subheader("Add New Game")
    
    # Initialize session state for form status
    if 'add_status' not in st.session_state:
        st.session_state.add_status = None
    
    # Create the form with fields for all game attributes
    with st.form("add_game_form"):
        # Basic game information
        game_name = st.text_input("Game Name*", help="Required")

        game_types_data = load_game_types()
        game_type_options = [gt['name'] for gt in game_types_data]
        game_type = st.selectbox("Game Type*", game_type_options, help="Select the type of game")


        difficulty = st.selectbox("Difficulty*", ["Easy", "Medium", "Hard"])
        
        # Player information
        col1, col2 = st.columns(2)
        with col1:
            min_players = st.number_input("Min Players*", min_value=1, value=2)
        with col2:
            max_players = st.number_input("Max Players*", min_value=min_players, value=max(4, min_players))
        
        # Age and duration
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Minimum Age*", min_value=0, value=8)
        with col2:
            min_duration = st.number_input("Duration (minutes)*", min_value=1, value=30)
        
        # Materials
        materials = st.text_area("Materials* (comma separated)", 
                               help="List materials needed, separated by commas")
        
        # Game details
        game_explanation = st.text_area("Game Explanation*", 
                                      help="Brief description of what the game is about")
        rules = st.text_area("Rules", 
                           help="Step-by-step explanation of how to play")
        score_calculation = st.text_area("Score Calculation", 
                                       help="How points are earned and winners determined")
        example = st.text_area("Example", 
                             help="A brief example of gameplay")
        
        # Optional fields
        expander = st.expander("Additional Options")
        with expander:
            expansions = st.text_area("Expansions (comma separated)", 
                                     help="Optional expansions for the game")
            drinking_rules = st.text_area("Drinking Rules (optional)", 
                                        help="Optional rules for adult drinking games")
        
        # Submit button
        submitted = st.form_submit_button("Add Game")
        
        if submitted:
            # Basic validation
            if not game_name or not game_type or not game_explanation:
                st.session_state.add_status = "error_validation"
                st.session_state.validation_message = "Please fill in all required fields (marked with *)."
            else:
                try:
                    # Prepare game data
                    new_game = {
                        'game_name': game_name,
                        'game_type': game_type,
                        'difficulty': difficulty,
                        'min_players': min_players,
                        'max_players': max_players,
                        'min_age': min_age,
                        'min_duration': min_duration,
                        'materials': [item.strip() for item in materials.split(',') if item.strip()],
                        'game_explanation': game_explanation,
                        'rules': rules,
                        'score_calculation': score_calculation,
                        'example': example,
                        'expansions': [item.strip() for item in expansions.split(',') if item.strip()],
                        'drinking_rules': drinking_rules,
                        'image_path': ""  # Empty for now, could be added later
                    }
                    
                    # Get Firestore database
                    db = get_firestore_db()
                    games_ref = db.collection("games")
                    
                    # Check if a game with this name already exists
                    existing_games = list(games_ref.where("game_name", "==", game_name).limit(1).stream())
                    if existing_games:
                        st.session_state.add_status = "error_duplicate"
                        st.session_state.duplicate_game = game_name
                    else:
                        # Add the new game
                        games_ref.add(new_game)
                        st.session_state.add_status = "success"
                        st.session_state.added_game_name = game_name
                
                except Exception as e:
                    st.session_state.add_status = "error"
                    st.session_state.add_error = str(e)
    
    # Display status messages based on session state
    if st.session_state.add_status == "success":
        st.success(f"'{st.session_state.added_game_name}' has been added successfully!")
        
        # Offer to add another game or clear form
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Another Game", key="add_another"):
                st.session_state.add_status = None
                st.session_state.added_game_name = None
                st.rerun()
        with col2:
            if st.button("View Games", key="view_games"):
                # Change to the main view games page
                st.session_state.current_page = "View Games"
                st.session_state.db_page = "main"  # Reset the database page
                st.rerun()
    
    elif st.session_state.add_status == "error_validation":
        st.error(st.session_state.validation_message)
        if st.button("OK", key="clear_validation"):
            st.session_state.add_status = None
    
    elif st.session_state.add_status == "error_duplicate":
        st.error(f"A game named '{st.session_state.duplicate_game}' already exists. Please use a different name.")
        if st.button("OK", key="clear_duplicate"):
            st.session_state.add_status = None
            st.session_state.duplicate_game = None
    
    elif st.session_state.add_status == "error":
        st.error(f"Error adding game: {st.session_state.add_error}")
        if st.button("OK", key="clear_add_error"):
            st.session_state.add_status = None
            st.session_state.add_error = None