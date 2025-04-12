import streamlit as st
from load_data import load_games  # Import load_games to get the games list

def view_games():
    """Display the list of games"""
    st.write(
        """
        Find the perfect game for your next gathering! Browse our collection of games
        and discover new favorites.
        """
    )

    # Load games (from Firebase or CSV)
    with st.spinner("Loading games..."):
        games = load_games()

    # Display games list
    if games:
        st.subheader(f"All Games ({len(games)})")
        
        # Create three columns for the games list
        cols = st.columns(3)
        
        # Display games in a grid with basic info
        for i, game in enumerate(games):
            with cols[i % 3]:
                with st.container():
                    st.subheader(game.get('game_name', 'Unnamed Game'))
                    st.caption(f"Type: {game.get('game_type', 'Not specified')}")
                    
                    # Game details button
                    if st.button("View Details", key=f"view_{game.get('id')}", use_container_width=True):
                        st.session_state['selected_game'] = game.get('id')
    else:
        st.info("No games found. Please add games to your Firebase database.")
