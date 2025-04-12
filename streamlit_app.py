import streamlit as st
from load_data import load_games  # Import the load_games function from the new file

# Set page configuration with title and icon
st.set_page_config(page_title="Games Database", page_icon="🎮", layout="wide")
st.title("🎮 Games Database")
st.write(
    """
    Find the perfect game for your next gathering! Browse our collection of games
    and discover new favorites.
    """
)

# Load games (from Firebase or CSV)
with st.spinner("Loading games..."):
    games = load_games()

# Display message only if Firebase is not initialized
if 'firebase_initialized' in st.session_state and not st.session_state['firebase_initialized']:
    st.warning("Failed to initialize Firebase. Showing demo data instead.")

# Display basic games list
if games:
    st.subheader(f"All Games ({len(games)})")
    
    # Create three columns for the games list
    cols = st.columns(3)
    
    # Display games in a grid with basic info
    for i, game in enumerate(games):
        with cols[i % 3]:
            with st.container(border=True):
                st.subheader(game.get('game_name', 'Unnamed Game'))
                st.caption(f"Type: {game.get('game_type', 'Not specified')}")
                
                # Game details button
                if st.button("View Details", key=f"view_{game.get('id')}", use_container_width=True):
                    st.session_state['selected_game'] = game.get('id')
else:
    st.info("No games found. Please add games to your Firebase database.")
    
    # Add a helpful message about setting up sample data
    with st.expander("Need help setting up sample data?"):
        st.markdown("""
        ### Sample Firebase Data Structure:
        
        Create a collection called `games` with documents containing these fields:
        
        ```
        game_name: "Uno"
        game_type: "Card"
        difficulty: "Easy"
        number_of_players: "2-10"
        age_range: "6+"
        duration: "30 min"
        materials: "UNO cards"
        game_explanation: "Match cards by color or number"
        ```
        """)

# Game detail view
if 'selected_game' in st.session_state:
    game_id = st.session_state['selected_game']
    selected_game = next((g for g in games if g.get('id') == game_id), None)
    
    if selected_game:
        with st.container(border=True):
            st.header(selected_game.get('game_name', 'Unnamed Game'))
            
            # Game information in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Info")
                st.write(f"**Type:** {selected_game.get('game_type', 'Not specified')}")
                st.write(f"**Difficulty:** {selected_game.get('difficulty', 'Not specified')}")
                st.write(f"**Players:** {selected_game.get('number_of_players', 'Not specified')}")
                st.write(f"**Age Range:** {selected_game.get('age_range', 'Not specified')}")
                st.write(f"**Duration:** {selected_game.get('duration', 'Not specified')}")
            
            with col2:
                st.subheader("Materials")
                st.write(selected_game.get('materials', 'Not specified'))
            
            # Game explanation
            st.subheader("Game Explanation")
            st.write(selected_game.get('game_explanation', 'No explanation provided.'))
            
            # Rules (if available)
            if 'rules' in selected_game and selected_game['rules']:
                st.subheader("Rules")
                st.write(selected_game['rules'])
            
            # Score calculation (if available)
            if 'score_calculation' in selected_game and selected_game['score_calculation']:
                st.subheader("Score Calculation")
                st.write(selected_game['score_calculation'])
            
            # Close button
            if st.button("Close Details", use_container_width=True):
                del st.session_state['selected_game']
                st.rerun()
