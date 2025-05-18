import streamlit as st
from firebase_config import get_firestore_db

def remove_user():
    st.subheader("Remove a User")

    db = get_firestore_db()
    users_ref = db.collection("users")

    # Load all users
    try:
        user_docs = list(users_ref.stream())
        usernames = [doc.to_dict().get("username", "unknown") for doc in user_docs]

        if not usernames:
            st.info("No users found.")
            return

        with st.form("delete_user_form"):
            selected_user = st.selectbox("Select a user to remove", usernames)
            confirm = st.checkbox("Confirm deletion of selected user")
            submitted = st.form_submit_button("Delete User")

            if submitted:
                if not confirm:
                    st.warning("Please confirm deletion before submitting.")
                else:
                    try:
                        for doc in user_docs:
                            if doc.to_dict().get("username") == selected_user:
                                doc.reference.delete()
                                st.success(f"User '{selected_user}' deleted successfully.")
                                st.rerun()
                        st.warning("User not found or already deleted.")
                    except Exception as e:
                        st.error(f"Error deleting user: {e}")
    except Exception as e:
        st.error(f"Could not fetch users: {e}")
