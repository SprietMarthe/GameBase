import streamlit as st
from firebase_config import get_firestore_db

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
            data.append({
                "Timestamp": record.get("timestamp", "—"),
                "Username": record.get("username", "—"),
                "Success": "✅" if record.get("success") else "❌",
                "IP": record.get("ip", "unknown")
            })

        st.dataframe(data, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load login attempts: {e}")
