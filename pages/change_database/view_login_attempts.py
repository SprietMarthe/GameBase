import streamlit as st
from firebase_config import get_firestore_db
from datetime import datetime


def view_login_attempts():
    st.subheader("Login Attempt Logs")

    db = get_firestore_db()
    attempts_ref = db.collection("login_attempts")

    try:
        docs = list(attempts_ref.order_by("timestamp", direction="DESCENDING").limit(50).stream())
        if not docs:
            st.info("No login attempts recorded.")
            return

        st.write("Most recent login attempts:")

        data = []
        for doc in docs:
            record = doc.to_dict()

            raw_timestamp = record.get("timestamp")
            if raw_timestamp:
                try:
                    dt = datetime.fromisoformat(raw_timestamp)
                    formatted_timestamp = dt.strftime("%d/%m/%Y %H:%M:%S")
                except ValueError:
                    formatted_timestamp = raw_timestamp  # fallback if parsing fails
            else:
                formatted_timestamp = "—"

            data.append({
                "Timestamp": formatted_timestamp,
                "Username": record.get("username", "—"),
                "Success": "✅" if record.get("success") else "❌",
            })

        st.dataframe(data, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load login attempts: {e}")
