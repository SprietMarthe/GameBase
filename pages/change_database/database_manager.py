import streamlit as st

from pages.change_database.add_game import add_game
from pages.change_database.delete_game import delete_game
from pages.change_database.edit_game import edit_game
from pages.change_database.add_user import add_user
from pages.change_database.remove_user import remove_user
from pages.change_database.view_login_attempts import view_login_attempts
from pages.change_database.view_visits import view_visits



def change_database():
    """CRUD Page for managing games (Add, Edit, Delete) and users"""

    if 'db_page' not in st.session_state:
        st.session_state.db_page = 'main'

    if st.session_state.db_page == 'main':
        st.subheader("Database Management")

        if st.session_state.get("admin_user_rights", False):
            st.write("Select an action to manage your games or users.")

            # 🎮 Game management buttons
            col1, col2, col3 = st.columns(3)
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

            # 👤 User management buttons
            st.markdown("---")
            st.subheader("User Management")

            col4, col5 = st.columns(2)
            with col4:
                if st.button("Add User", use_container_width=True):
                    st.session_state.db_page = 'add_user'
                    st.rerun()
            with col5:
                if st.button("Remove User", use_container_width=True):
                    st.session_state.db_page = 'remove_user'
                    st.rerun()

            # 📊 Analytics
            st.markdown("---")
            st.subheader("Analytics")

            col6, col7 = st.columns(2)
            with col6:
                if st.button("View Login Attempts", use_container_width=True):
                    st.session_state.db_page = 'view_login_attempts'
                    st.rerun()
            with col7:
                if st.button("View Visits", use_container_width=True):
                    st.session_state.db_page = 'view_visits'
                    st.rerun()

        # 🚪 Log out button (always visible)
        st.markdown("---")
        if st.button("🔒 Log Out", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    else:
        if st.button("← Back to Database Menu"):
            st.session_state.db_page = 'main'
            st.rerun()

    # Route to selected page
    if st.session_state.db_page == 'add':
        add_game()
    elif st.session_state.db_page == 'edit':
        edit_game()
    elif st.session_state.db_page == 'delete':
        delete_game()
    elif st.session_state.db_page == 'add_user':
        add_user()
    elif st.session_state.db_page == 'remove_user':
        remove_user()
    elif st.session_state.db_page == 'view_login_attempts':
        view_login_attempts()
    elif st.session_state.db_page == 'view_visits':
        view_visits()
