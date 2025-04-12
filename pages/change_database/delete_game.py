import streamlit as st
from load_data import load_games
from firebase_config import get_firestore_db

def delete_game():
    """Form to delete a game"""
    st.subheader("Delete a Game")
    
    # Load games to select which one to delete
    games = load_games()
    
    if not games:
        st.error("No games available to delete.")
        return
    
    # Initialize session state variables for deletion process
    if 'delete_game_selected' not in st.session_state:
        st.session_state.delete_game_selected = None
    
    if 'delete_status' not in st.session_state:
        st.session_state.delete_status = None
    
    # Extract game names for the dropdown
    game_names = [game.get('game_name', 'Unnamed Game') for game in games]
    
    # Game selection dropdown
    selected_game = st.selectbox(
        "Select Game to Delete", 
        options=game_names,
        index=0 if st.session_state.delete_game_selected is None else 
              game_names.index(st.session_state.delete_game_selected) 
              if st.session_state.delete_game_selected in game_names else 0,
        key="delete_game_selectbox"
    )
    
    # Update the selected game in session state
    st.session_state.delete_game_selected = selected_game
    
    # Display game information and confirmation
    if selected_game:
        # Find the full game data
        game_to_delete = next((game for game in games if game.get('game_name') == selected_game), None)
        
        if game_to_delete:
            # Display game information for confirmation
            st.warning(f"You are about to delete: **{selected_game}**")
            
            # Display some details about the game
            st.info(f"Type: {game_to_delete.get('game_type', 'Not specified')}")
            
            # Confirmation checkbox for safety
            confirm_delete = st.checkbox("I understand this action cannot be undone", key="confirm_delete")
            
            if confirm_delete:
                # Only show delete button if checkbox is checked
                if st.button("Delete Game", key="delete_game_button"):
                    try:
                        # Get Firestore database
                        db = get_firestore_db()
                        games_ref = db.collection("games")
                        
                        # Query for the game document
                        query = games_ref.where("game_name", "==", selected_game).limit(1).stream()
                        
                        # Find and delete the document
                        doc_found = False
                        for doc in query:
                            doc.reference.delete()
                            doc_found = True
                            break
                        
                        if doc_found:
                            # Update status in session state
                            st.session_state.delete_status = "success"
                            st.session_state.deleted_game_name = selected_game
                            # Reset selection
                            st.session_state.delete_game_selected = None
                        else:
                            st.session_state.delete_status = "error_not_found"
                        
                    except Exception as e:
                        st.session_state.delete_status = "error"
                        st.session_state.delete_error = str(e)
    
    # Display status messages based on session state
    if st.session_state.delete_status == "success":
        st.success(f"'{st.session_state.deleted_game_name}' has been deleted successfully!")
        if st.button("Clear", key="clear_success"):
            st.session_state.delete_status = None
            st.session_state.deleted_game_name = None
            # Rerun to refresh the game list
            st.rerun()
    
    elif st.session_state.delete_status == "error_not_found":
        st.error(f"Game not found in database. It may have been already deleted.")
        if st.button("Clear", key="clear_error_not_found"):
            st.session_state.delete_status = None
    
    elif st.session_state.delete_status == "error":
        st.error(f"Error deleting game: {st.session_state.delete_error}")
        if st.button("Clear", key="clear_error"):
            st.session_state.delete_status = None
            st.session_state.delete_error = None