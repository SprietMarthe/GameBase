import streamlit as st

def add_game():
    """Page for adding/updating games"""
    
    st.subheader("Add/Update Games")
    # Form for adding/updating games
    with st.form("game_form"):
        game_name = st.text_input("Game Name")
        game_type = st.text_input("Game Type")
        difficulty = st.text_input("Difficulty")
        number_of_players = st.text_input("Number of Players")
        age_range = st.text_input("Age Range")
        duration = st.text_input("Duration")
        materials = st.text_input("Materials")
        game_explanation = st.text_area("Game Explanation")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Game added successfully!")
            # Add code to save the data to Firebase or a CSV
