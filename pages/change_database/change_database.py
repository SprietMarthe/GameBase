import streamlit as st

from pages.change_database.add_game import add_game
from pages.change_database.delete_game import delete_game
from pages.change_database.edit_game import edit_game

def change_database():
    """CRUD Page for managing games (Add, Edit, Delete)"""
    
    # Horizontal menu for CRUD options, using columns for a consistent layout
    col1, col2, col3 = st.columns([1, 1, 1])  # Three equally sized columns

    with col1:
        add_game_button = st.button("Add Game", use_container_width=True)

    with col2:
        edit_game_button = st.button("Edit Game", use_container_width=True)

    with col3:
        delete_game_button = st.button("Delete Game", use_container_width=True)

    # Now handle what happens based on the button clicked
    if add_game_button:
        add_game()  # Display Add Game form
    
    elif edit_game_button:
        edit_game()  # Display Edit Game form

    elif delete_game_button:
        delete_game()  # Display Delete Game form