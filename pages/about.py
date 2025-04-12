import streamlit as st

def about():
    """About the app"""
    st.subheader("About GameBase")
    st.write(
        """
        Welcome to **GameBase**!

        GameBase allows you to browse a collection of games for various occasions.
        It is a database for games :).
        As the developer, you can add or update the games in the database through the settings.
        """
    )
