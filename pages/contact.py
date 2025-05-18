import streamlit as st
from firebase_config import get_firestore_db
from datetime import datetime, timezone
from google.cloud.firestore_v1 import FieldFilter

def contact():
    st.subheader("Submit Your Game Idea")

    db = get_firestore_db()
    session_id = st.session_state.get("anonymous_id", "unknown")
    today_str = datetime.now(timezone.utc).date().isoformat()

    # Check how many submissions this session made today
    submissions_ref = db.collection("game_suggestions")
    existing_submissions = list(
        submissions_ref
        .where(filter=FieldFilter("session_id", "==", session_id))
        .where(filter=FieldFilter("date", "==", today_str))
        .stream()
    )

    if len(existing_submissions) >= 5:
        st.warning("You’ve reached the submission limit of 5 for today. Please try again tomorrow.")
        return

    with st.form("submit_game_form"):
        name = st.text_input("Your Name*", key="contact_name")
        email = st.text_input("Your Email (optional)", key="contact_email")
        game_name = st.text_input("Proposed Game Name", key="contact_game_name")
        idea = st.text_area("Describe Your Game Idea*", height=200, key="contact_idea")
        follow_up = st.checkbox("I’d like to be contacted if you use my idea", key="contact_follow_up")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not idea.strip():
                st.error("Please describe your game idea.")
            else:
                submissions_ref.add({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "date": today_str,
                    "session_id": session_id,
                    "name": name.strip(),
                    "email": email.strip(),
                    "game_name": game_name.strip(),
                    "idea": idea.strip(),
                    "follow_up": follow_up
                })
                st.success("Thank you! Your game idea has been submitted.")

                # Clear form fields
                for key in [
                    "contact_name", "contact_email", "contact_game_name",
                    "contact_idea", "contact_follow_up"
                ]:
                    st.session_state.pop(key, None)

                st.rerun()
