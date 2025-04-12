import streamlit as st

from pages.change_database.add_game import add_game
from pages.change_database.delete_game import delete_game
from pages.change_database.edit_game import edit_game

def change_database():
    """CRUD Page for managing games (Add, Edit, Delete)"""
    
    # Initialize the database page state if it doesn't exist
    if 'db_page' not in st.session_state:
        st.session_state.db_page = 'main'
    
    # Only show the menu buttons if we're on the main page
    if st.session_state.db_page == 'main':
        st.subheader("Database Management")
        st.write("Select an action to manage your games database.")
        
        # Horizontal menu for CRUD options
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Add Game", use_container_width=True):
                st.session_state.db_page = 'add'
                st.rerun()
        
        with col2:
            if st.button("Edit Game", use_container_width=True):
                st.session_state.db_page = 'edit'
                st.rerun()
        
        with col3:
            if st.button("Delete Game", use_container_width=True):
                st.session_state.db_page = 'delete'
                st.rerun()
    else:
        # Show a back button when not on the main page
        if st.button("← Back to Database Menu"):
            st.session_state.db_page = 'main'
            st.rerun()
    
    # Render the appropriate page based on the session state
    if st.session_state.db_page == 'add':
        add_game()
    elif st.session_state.db_page == 'edit':
        edit_game()
    elif st.session_state.db_page == 'delete':
        delete_game()