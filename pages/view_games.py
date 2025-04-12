import streamlit as st
from load_data import load_games

def search_and_filter_games(games, search_term, difficulty=None, min_players=None, max_players=None):
    """
    Search and filter games by various criteria
    
    Parameters:
    - games: list of game dictionaries
    - search_term: string to search for
    - difficulty: filter by game difficulty
    - min_players: minimum number of players
    - max_players: maximum number of players
    
    Returns:
    - filtered list of games matching all criteria
    """
    filtered_games = games.copy()
    
    # Apply search term if provided
    if search_term:
        search_term = search_term.lower()
        search_results = []
        
        for game in filtered_games:
            # Search in name, type, or explanation
            if (search_term in game.get('game_name', '').lower() or
                search_term in game.get('game_type', '').lower() or
                search_term in game.get('game_explanation', '').lower()):
                search_results.append(game)
                continue
                
            # Search in materials (which might be a list)
            materials = game.get('materials', [])
            if isinstance(materials, list):
                for material in materials:
                    if search_term in material.lower():
                        search_results.append(game)
                        break
        
        filtered_games = search_results
    
    # Filter by difficulty
    if difficulty and difficulty != "All":
        filtered_games = [game for game in filtered_games 
                         if game.get('difficulty') == difficulty]
    
    # Filter by player count
    if min_players is not None:
        filtered_games = [game for game in filtered_games 
                         if game.get('min_players', 0) <= min_players <= game.get('max_players', 999)]
    
    if max_players is not None:
        filtered_games = [game for game in filtered_games 
                         if game.get('min_players', 0) <= max_players <= game.get('max_players', 999)]
    
    return filtered_games

def view_games():
    """Display the games database with search and filtering options"""
    st.title("Games Database")
    
    # Load all games
    all_games = load_games()
    
    if not all_games:
        st.info("No games found in the database. Add some games to get started!")
        return
    
    # Initialize session state for filters
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "All"
    if 'player_count' not in st.session_state:
        st.session_state.player_count = 4  # Default player count
    
    # Create a container for filters
    with st.container():
        st.subheader("Find Your Perfect Game")
        
        # Two columns for search and difficulty
        col1, col2 = st.columns(2)
        
        with col1:
            # Search box
            search_term = st.text_input(
                "Search by name or description",
                value=st.session_state.search_term,
                placeholder="Type to search...",
                key="game_search"
            )
            
            if search_term != st.session_state.search_term:
                st.session_state.search_term = search_term
        
        with col2:
            # Difficulty filter
            difficulty_options = ["All", "Easy", "Medium", "Hard"]
            selected_difficulty = st.selectbox(
                "Difficulty", 
                options=difficulty_options,
                index=difficulty_options.index(st.session_state.selected_difficulty),
                key="difficulty_filter"
            )
            
            if selected_difficulty != st.session_state.selected_difficulty:
                st.session_state.selected_difficulty = selected_difficulty
        
        # Players filter
        max_players_in_games = 12  # Default fallback value
        for game in all_games:
            max_game_players = game.get('max_players', 0)
            if isinstance(max_game_players, (int, float)) and max_game_players > max_players_in_games:
                max_players_in_games = max_game_players
        # Ensure the max is at least the default of 12
        max_players_slider = max(12, max_players_in_games)
        player_count = st.slider(
            "Number of Players",
            min_value=1,
            max_value=max_players_slider,
            value=min(st.session_state.player_count, max_players_slider),
            key="player_count_filter"
        )
        
        if player_count != st.session_state.player_count:
            st.session_state.player_count = player_count
        
        # Clear filters button
        if st.button("Clear Filters"):
            st.session_state.search_term = ""
            st.session_state.selected_difficulty = "All"
            st.session_state.player_count = 4
            st.rerun()
    
    # Apply filters and search
    filtered_games = search_and_filter_games(
        all_games, 
        st.session_state.search_term,
        st.session_state.selected_difficulty if st.session_state.selected_difficulty != "All" else None,
        st.session_state.player_count,
        st.session_state.player_count
    )
    
    # Display filter statistics
    st.write(f"Found {len(filtered_games)} of {len(all_games)} games matching your criteria")
    
    # Display games
    if filtered_games:
        # Create a grid layout for games
        cols = st.columns(3)  # Display games in 3 columns
        
        for i, game in enumerate(filtered_games):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(game.get('game_name', 'Unnamed Game'))
                    st.caption(f"Type: {game.get('game_type', 'Not specified')}")
                    
                    # Display basic game info
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Players:** {game.get('min_players', '-')} - {game.get('max_players', '-')}")
                        st.write(f"**Duration:** {game.get('min_duration', '-')} min")
                    with col2:
                        st.write(f"**Difficulty:** {game.get('difficulty', 'Not specified')}")
                        st.write(f"**Age:** {game.get('min_age', '-')}+")
                    
                    # View details button
                    if st.button("View Details", key=f"view_{i}"):
                        st.session_state.selected_game = game
                        st.rerun()
    else:
        st.warning("No games found matching your search criteria.")
    
    # Display detailed view if a game is selected
    if 'selected_game' in st.session_state and st.session_state.selected_game:
        display_game_details(st.session_state.selected_game)

def display_game_details(game):
    """Display detailed information about a selected game"""
    with st.container(border=True):
        # Header with close button
        col1, col2 = st.columns([5, 1])
        with col1:
            st.header(game.get('game_name', 'Unnamed Game'))
        with col2:
            if st.button("Close", key="close_details"):
                del st.session_state.selected_game
                st.rerun()
        
        # Display detailed game information
        st.subheader("Game Information")
        
        # Basic info in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Type:** {game.get('game_type', 'Not specified')}")
            st.write(f"**Difficulty:** {game.get('difficulty', 'Not specified')}")
        with col2:
            st.write(f"**Players:** {game.get('min_players', '-')} - {game.get('max_players', '-')}")
            st.write(f"**Min Age:** {game.get('min_age', '-')}+")
        with col3:
            st.write(f"**Duration:** {game.get('min_duration', '-')} min")
        
        # Game explanation
        st.subheader("Game Explanation")
        st.write(game.get('game_explanation', 'No explanation available.'))
        
        # Materials needed
        st.subheader("Materials Needed")
        materials = game.get('materials', [])
        if materials:
            if isinstance(materials, list):
                for material in materials:
                    st.write(f"- {material}")
            else:
                st.write(materials)
        else:
            st.write("No materials specified.")
        
        # Rules (if available)
        if game.get('rules'):
            st.subheader("Rules")
            st.write(game.get('rules'))
        
        # Score calculation (if available)
        if game.get('score_calculation'):
            st.subheader("Score Calculation")
            st.write(game.get('score_calculation'))
        
        # Example (if available)
        if game.get('example'):
            st.subheader("Example")
            st.write(game.get('example'))
        
        # Expansions (if available)
        expansions = game.get('expansions', [])
        if expansions and (isinstance(expansions, list) and len(expansions) > 0 or isinstance(expansions, str) and expansions.strip()):
            st.subheader("Expansions")
            if isinstance(expansions, list):
                for expansion in expansions:
                    st.write(f"- {expansion}")
            else:
                st.write(expansions)
        
        # Drinking rules (if available and user is of legal age)
        if game.get('drinking_rules'):
            with st.expander("Drinking Rules (21+ only)"):
                st.write(game.get('drinking_rules'))