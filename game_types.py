import streamlit as st
from firebase_config import get_firestore_db

def setup_game_types():
    """Initialize game types in Firebase if they don't exist"""
    try:
        db = get_firestore_db()
        
        # Default game types
        default_types = [
            {"name": "Card Game", "order": 1},
            {"name": "Board Game", "order": 2},
            {"name": "Puzzle Game", "order": 3},
            {"name": "Adventure Game", "order": 4},
            {"name": "Party Game", "order": 5},
            {"name": "Other", "order": 6}
        ]
        
        # Check if game_types collection exists and has documents
        types_ref = db.collection("game_types")
        existing_types = list(types_ref.limit(1).stream())
        
        if not existing_types:
            # Add the default types
            for game_type in default_types:
                types_ref.add(game_type)
            st.success("Game types initialized successfully!")
        
        return True
    except Exception as e:
        st.error(f"Error setting up game types: {e}")
        return False

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_game_types():
    """Fetch game types from Firestore database"""
    try:
        db = get_firestore_db()
        types_ref = db.collection("game_types")
        # Order by the order field
        types_docs = types_ref.order_by("order").stream()
        
        game_types = []
        for doc in types_docs:
            type_data = doc.to_dict()
            type_data['id'] = doc.id  # Add the document ID
            game_types.append(type_data)
            
        return game_types
    except Exception as e:
        st.error(f"Error loading game types: {e}")
        return []
    

def manage_game_types():
    """Section for managing game types"""
    st.subheader("Manage Game Types")
    
    # Initialize game types if needed
    setup_game_types()
    
    # Load game types
    game_types = load_game_types()
    
    # Display existing game types
    st.write("Current Game Types:")
    
    for i, game_type in enumerate(game_types):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i+1}. {game_type['name']}")
        with col2:
            if game_type['name'] != "Other":  # Don't allow deleting "Other"
                if st.button("Delete", key=f"del_type_{game_type['id']}"):
                    try:
                        db = get_firestore_db()
                        db.collection("game_types").document(game_type['id']).delete()
                        st.success(f"Game type '{game_type['name']}' deleted!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting game type: {e}")
    
    # Add new game type
    st.write("Add New Game Type:")
    with st.form("add_game_type_form"):
        new_type_name = st.text_input("Type Name")
        submitted = st.form_submit_button("Add Game Type")
        
        if submitted and new_type_name:
            try:
                # Check if this type already exists
                if any(gt['name'] == new_type_name for gt in game_types):
                    st.error(f"Game type '{new_type_name}' already exists!")
                else:
                    # Add the new type
                    db = get_firestore_db()
                    new_order = max([gt.get('order', 0) for gt in game_types], default=0) + 1
                    db.collection("game_types").add({
                        "name": new_type_name,
                        "order": new_order
                    })
                    st.success(f"Game type '{new_type_name}' added!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error adding game type: {e}")