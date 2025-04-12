# helpers.py

import streamlit as st
import pandas as pd

def format_game_duration(duration):
    """Format the game duration to be more readable."""
    if isinstance(duration, str) and "min" in duration:
        return duration.replace("min", " minutes")
    return duration


def custom_header(title: str):
    """Display a custom header with the game icon."""
    st.title(f"🎮 {title}")
    st.markdown("---")