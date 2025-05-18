import streamlit as st
from firebase_config import get_firestore_db
from game_types import load_game_types
from datetime import datetime, timezone


def add_game():
    """Form for adding a new game to the database"""
    st.subheader("Add New Game")
    
    # Initialize session state for form status
    if 'add_status' not in st.session_state:
        st.session_state.add_status = None

    if st.session_state.get("reset_form"):
        for key in [
            "game_name", "game_type", "difficulty", "min_players", "max_players",
            "min_age", "min_duration", "materials", "game_explination", "rules",
            "score_calculation", "example", "expansions", "drinking_rules"
        ]:
            st.session_state.pop(key, None)
        st.session_state.reset_form = False
    
    # Create the form with fields for all game attributes
    with st.form("add_game_form"):
        # Basic game information
        game_name = st.text_input("Game Name*", help="Required", key="game_name")

        game_types_data = load_game_types()
        game_type_options = [gt['name'] for gt in game_types_data]
        game_type = st.selectbox("Game Type*", game_type_options, help="Select the type of game", key="game_type")


        difficulty = st.selectbox("Difficulty*", ["Easy", "Medium", "Hard"], key="difficulty")
        
        # Player information
        col1, col2 = st.columns(2)
        with col1:
            min_players = st.number_input("Min Players*", min_value=1, value=2, key="min_players")
        with col2:
            max_players = st.number_input("Max Players*", min_value=min_players, value=max(4, min_players), key="max_players")
        
        # Age and duration
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Minimum Age*", min_value=0, value=8, key="min_age")
        with col2:
            min_duration = st.number_input(
                "Duration (minutes)*",
                min_value=15,
                max_value=480,
                step=15,
                value=30,
                help="Use 15-minute steps",
                key="min_duration"
            )
        
        # Materials
        # Automatically suggest "deck of cards" if "Card Game" is selected
        default_materials = "Deck of cards" if game_type == "Card Game" else ""
        materials = st.text_area(
            "Materials* (comma separated)",
            value=default_materials,
            help="List materials needed, separated by commas",
            key="materials"
        )
        
        # Game details
        game_explanation = st.text_area("Game Explanation*", key="game_explination",
                                      help="Brief description of what the game is about")
        rules = st.text_area("Rules", height=150, key="rules",
                           help="Step-by-step explanation of how to play")
        score_calculation = st.text_area("Score Calculation", height=120, key="score_calculation",
                                       help="How points are earned and winners determined")
        example = st.text_area("Example", height=150, key="example",
                             help="A brief example of gameplay")
        
        # Determine if the form is incomplete
        required_fields = [game_name, game_type, game_explanation]
        auto_flag = not all(required_fields)

        # Let user override the flag (default based on missing required fields)
        manual_flag = st.checkbox("Mark this game as incomplete (to finish later)", value=auto_flag)

        
        # Optional fields
        expander = st.expander("Additional Options")
        with expander:
            expansions = st.text_area("Expansions (comma separated)", height=120, key="expansions",
                                     help="Optional expansions for the game")
            drinking_rules = st.text_area("Drinking Rules (optional)", height=120, key="drinking_rules",
                                        help="Optional rules for adult drinking games")
        

        # Submit button
        submitted = st.form_submit_button("Add Game")
        
        if submitted:
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
                    'materials': [item.strip().title() for item in materials.split(',') if item.strip()],
                    'game_explanation': game_explanation,
                    'rules': rules,
                    'score_calculation': score_calculation,
                    'example': example,
                    'expansions': [item.strip().upper() for item in expansions.split(',') if item.strip()],
                    'drinking_rules': drinking_rules,
                    'to_be_updated': manual_flag,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "created_by": st.session_state.get("username", "unknown"),
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
                st.session_state.reset_form = True
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