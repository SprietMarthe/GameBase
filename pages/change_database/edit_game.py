import streamlit as st
from game_types import load_game_types
from load_data import load_games
from firebase_config import get_firestore_db
from datetime import datetime, timezone

def edit_game():
    st.subheader("Edit an Existing Game")

    if 'edit_game_selected' not in st.session_state:
        st.session_state.edit_game_selected = None

    if 'edit_status' not in st.session_state:
        st.session_state.edit_status = None

    games = load_games()
    games = sorted(games, key=lambda g: g.get('to_be_updated', False), reverse=True)

    if not games:
        st.error("No games available to edit.")
        return

    game_names = [game.get('game_name', 'Unnamed Game') for game in games]

    selected_game = st.selectbox(
        "Select Game to Edit",
        options=game_names,
        index=0 if st.session_state.edit_game_selected is None else
              game_names.index(st.session_state.edit_game_selected)
              if st.session_state.edit_game_selected in game_names else 0,
        key="edit_game_selectbox"
    )

    st.session_state.edit_game_selected = selected_game

    if selected_game:
        game = next((game for game in games if game.get('game_name') == selected_game), None)

        if game:
            with st.form("edit_game_form"):
                st.subheader(f"Editing: {selected_game}")

                new_game_name = st.text_input("Game Name", game.get('game_name', ''))

                game_types_data = load_game_types()
                game_type_options = [gt['name'] for gt in game_types_data]
                current_type = game.get('game_type', '')
                is_other_type = not any(current_type == option for option in game_type_options)
                other_type_value = ""

                if is_other_type and current_type.startswith("Other: "):
                    other_type_value = current_type[7:]
                    selected_index = game_type_options.index("Other")
                else:
                    selected_index = game_type_options.index(current_type) if current_type in game_type_options else 0

                new_game_type = st.selectbox("Game Type", game_type_options, index=selected_index)

                if new_game_type == "Other":
                    other_type = st.text_input("Please specify game type", value=other_type_value)
                    if other_type:
                        new_game_type = f"Other: {other_type}"

                new_difficulty = st.selectbox("Difficulty",
                                              ["Easy", "Medium", "Hard"],
                                              index=["Easy", "Medium", "Hard"].index(game.get('difficulty', 'Medium')))

                col1, col2 = st.columns(2)
                with col1:
                    new_min_players = st.number_input("Min Players", min_value=1, value=game.get('min_players', 1))
                with col2:
                    new_max_players = st.number_input("Max Players", min_value=1,
                                                      value=max(game.get('max_players', 8), new_min_players))
                if new_max_players < new_min_players:
                    new_max_players = new_min_players
                    
                col1, col2 = st.columns(2)
                with col1:
                    new_min_age = st.number_input("Minimum Age", min_value=0, value=game.get('min_age', 8))
                with col2:
                    new_min_duration = st.number_input("Duration (minutes)",
                                                       min_value=15,
                                                       max_value=480,
                                                       step=15,
                                                       value=max(15, game.get('min_duration', 30)))

                materials_list = game.get('materials', [])
                if isinstance(materials_list, str):
                    materials_list = [item.strip().title() for item in materials_list.split(',') if item.strip()]
                if game.get('game_type') == "Card Game" and "deck of cards" not in [m.lower() for m in materials_list]:
                    materials_list.append("deck of cards")
                materials_default = ', '.join(materials_list)
                new_materials = st.text_area("Materials (comma separated)", materials_default)

                new_game_explanation = st.text_area("Game Explanation", game.get('game_explanation', ''))
                new_rules = st.text_area("Rules", game.get('rules', ''))
                new_score_calculation = st.text_area("Score Calculation", game.get('score_calculation', ''))
                new_example = st.text_area("Example", game.get('example', ''))

                incomplete_flag = game.get('to_be_updated', False)
                new_to_be_updated = st.checkbox("Mark this game as incomplete", value=incomplete_flag)

                expander = st.expander("Additional Options")
                with expander:
                    new_expansions = st.text_area("Expansions (comma separated)",
                                                  ', '.join(game.get('expansions', []))
                                                  if isinstance(game.get('expansions'), list)
                                                  else game.get('expansions', ''))
                    new_drinking_rules = st.text_area("Drinking Rules (optional)", game.get('drinking_rules', ''))

                submitted = st.form_submit_button("Save Changes")

                if submitted:
                    try:
                        updated_game = {
                            'game_name': new_game_name,
                            'game_type': new_game_type,
                            'difficulty': new_difficulty,
                            'min_players': new_min_players,
                            'max_players': new_max_players,
                            'min_age': new_min_age,
                            'min_duration': new_min_duration,
                            'materials': [item.strip() for item in new_materials.split(',') if item.strip()],
                            'game_explanation': new_game_explanation,
                            'rules': new_rules,
                            'score_calculation': new_score_calculation,
                            'example': new_example,
                            'expansions': [item.strip() for item in new_expansions.split(',') if item.strip()],
                            'drinking_rules': new_drinking_rules,
                            'to_be_updated': new_to_be_updated
                        }

                        # Compare changes
                        changes = {}
                        for key in updated_game:
                            old = game.get(key)
                            new = updated_game[key]
                            if old != new:
                                changes[key] = {"old": old, "new": new}

                        db = get_firestore_db()
                        games_ref = db.collection("games")
                        query = games_ref.where("game_name", "==", selected_game).limit(1).stream()


                        # Fill in created_by and created_at if they are missing in the current game document
                        if not game.get("created_by"):
                            updated_game["created_by"] = st.session_state.get("username", "unknown")
                        if not game.get("created_at"):
                            updated_game["created_at"] = datetime.now(timezone.utc).isoformat()

                        doc_found = False
                        for doc in query:
                            doc.reference.update(updated_game)
                            doc_found = True

                            # Log the update to a separate collection
                            if changes:
                                db.collection("game_update_logs").add({
                                    "game_id": doc.id,
                                    "updated_by": st.session_state.get("username", "unknown"),
                                    "updated_at": datetime.now(timezone.utc).isoformat(),
                                    "changes": changes
                                })
                            break

                        if doc_found:
                            updated_games = load_games()
                            st.session_state.edit_game_selected = new_game_name
                            st.session_state.games_cache = updated_games  # optional: cache

                            st.session_state.edit_status = "success"
                            st.session_state.edited_game_name = new_game_name
                            st.rerun()  # force rerender to load fresh data
                        else:
                            st.session_state.edit_status = "error_not_found"

                    except Exception as e:
                        st.session_state.edit_status = "error"
                        st.session_state.edit_error = str(e)

        else:
            st.error(f"Could not find data for game: {selected_game}")

    if st.session_state.edit_status == "success":
        st.success(f"'{st.session_state.edited_game_name}' has been updated successfully!")
        if st.button("Clear", key="clear_edit_success"):
            st.session_state.edit_status = None
            st.session_state.edited_game_name = None
            st.rerun()

    elif st.session_state.edit_status == "error_not_found":
        st.error(f"Game not found in database. It may have been deleted.")
        if st.button("Clear", key="clear_edit_error_not_found"):
            st.session_state.edit_status = None

    elif st.session_state.edit_status == "error":
        st.error(f"Error updating game: {st.session_state.edit_error}")
        if st.button("Clear", key="clear_edit_error"):
            st.session_state.edit_status = None
            st.session_state.edit_error = None
