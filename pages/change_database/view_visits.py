import streamlit as st
from firebase_config import get_firestore_db
from datetime import datetime
import pandas as pd

def view_visits():
    st.subheader("Visitor Timeline")

    db = get_firestore_db()
    logs_ref = db.collection("visit_logs").order_by("timestamp")
    entries = list(logs_ref.stream())

    rows = []
    for doc in entries:
        data = doc.to_dict()
        ts_str = data.get("timestamp")
        try:
            date = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).date()
        except:
            continue

        rows.append({
            "Date": date,
            "Username": data.get("username", "anonymous"),
            "Admin": data.get("is_admin", False)
        })

    if not rows:
        st.info("No visit logs found.")
        return

    df = pd.DataFrame(rows)

    # Determine full date range
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    all_dates = pd.date_range(start=min_date, end=max_date).date

    # Count admin and user visits
    admin_df = df[df["Admin"]].groupby("Date").size().reindex(all_dates, fill_value=0)
    user_df = df[~df["Admin"]].groupby("Date").size().reindex(all_dates, fill_value=0)

    chart_data = pd.DataFrame({
        "Admin Visits": admin_df,
        "User Visits": user_df
    })

    # Make chart scrollable horizontally
    st.markdown("### Visits Over Time (Admins vs Users)")
    st.line_chart(chart_data)

    # Show exact numbers in a table
    st.markdown("### Raw Visit Counts")
    st.dataframe(chart_data)