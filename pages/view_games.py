import streamlit as st
from load_data import load_games

def search_and_filter_games(games, search_term, difficulty=None, min_players=None, max_players=None, drinking_only=False):
    filtered_games = games.copy()

    if search_term:
        search_term = search_term.lower()
        search_results = []

        for game in filtered_games:
            if (search_term in game.get('game_name', '').lower() or
                search_term in game.get('game_type', '').lower() or
                search_term in game.get('game_explanation', '').lower()):
                search_results.append(game)
                continue

            materials = game.get('materials', [])
            if isinstance(materials, list):
                for material in materials:
                    if search_term in material.lower():
                        search_results.append(game)
                        break

        filtered_games = search_results

    if difficulty and difficulty != "All":
        filtered_games = [game for game in filtered_games 
                         if game.get('difficulty') == difficulty]

    if min_players is not None:
        filtered_games = [game for game in filtered_games 
                         if game.get('min_players', 0) <= min_players <= game.get('max_players', 999)]

    if max_players is not None:
        filtered_games = [game for game in filtered_games 
                         if game.get('min_players', 0) <= max_players <= game.get('max_players', 999)]

    if drinking_only:
        filtered_games = [
            game for game in filtered_games
            if ("drink" in game.get('game_explanation', '').lower())
            or game.get('drinking_rules', '').strip()
        ]

    return filtered_games


def view_games():
    """Display the games database with search and filtering options"""
    st.title("Game Database")

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "list"

    if "selected_game" not in st.session_state:
        st.session_state.selected_game = None

    all_games = load_games()

    if not all_games:
        st.info("No games found in the database. Add some games to get started!")
        return

    if st.session_state.view_mode == "details":
        display_game_details(st.session_state.selected_game)
        return

    # Initialize session state for filters
    if 'search_term' not in st.session_state:
        st.session_state.search_term = ""
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = "All"
    if 'player_count' not in st.session_state:
        st.session_state.player_count = 4
    if 'drinking_filter' not in st.session_state:
        st.session_state.drinking_filter = False

    with st.container():
        st.subheader("Find Your Perfect Game")

        col1, col2 = st.columns(2)

        with col1:
            search_term = st.text_input(
                "Search by name or description",
                value=st.session_state.search_term,
                placeholder="Type to search...",
                key="game_search"
            )
            st.session_state.search_term = search_term

        with col2:
            difficulty_options = ["All", "Easy", "Medium", "Hard"]
            selected_difficulty = st.selectbox(
                "Difficulty", 
                options=difficulty_options,
                index=difficulty_options.index(st.session_state.selected_difficulty),
                key="difficulty_filter"
            )
            st.session_state.selected_difficulty = selected_difficulty

        st.checkbox(
            "Only show drinking games",
            value=st.session_state.drinking_filter,
            key="drinking_filter"
        )

        max_players_in_games = max(
            [game.get('max_players', 0) for game in all_games if isinstance(game.get('max_players'), (int, float))],
            default=12
        )
        max_players_slider = max(12, max_players_in_games)

        player_count = st.slider(
            "Number of Players",
            min_value=1,
            max_value=max_players_slider,
            value=min(st.session_state.player_count, max_players_slider),
            key="player_count_filter"
        )
        st.session_state.player_count = player_count

        if st.button("Clear Filters"):
            st.session_state.search_term = ""
            st.session_state.selected_difficulty = "All"
            st.session_state.player_count = 4
            st.session_state.drinking_filter = False
            st.rerun()

    filtered_games = search_and_filter_games(
        all_games, 
        st.session_state.search_term,
        st.session_state.selected_difficulty if st.session_state.selected_difficulty != "All" else None,
        st.session_state.player_count,
        st.session_state.player_count,
        st.session_state.drinking_filter
    )

    st.write(f"Found {len(filtered_games)} of {len(all_games)} games matching your criteria")

    if filtered_games:
        cols = st.columns(3)
        for i, game in enumerate(filtered_games):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(game.get('game_name', 'Unnamed Game'))
                    st.caption(f"Type: {game.get('game_type', 'Not specified')}")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Players:** {game.get('min_players', '-')} - {game.get('max_players', '-')}")
                        st.write(f"{game.get('min_duration', '-')} min")
                    with col2:
                        st.write(f"**Difficulty:** {game.get('difficulty', 'Not specified')}")

                    if st.button("View Details", key=f"view_{i}"):
                        st.session_state.selected_game = game
                        st.session_state.view_mode = "details"
                        st.rerun()
    else:
        st.warning("No games found matching your search criteria.")


def display_game_details(game):
    """Display detailed information about a selected game"""
    with st.container(border=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.header(game.get('game_name', 'Unnamed Game'))
        with col2:
            if st.button("← Back to Game List", key="close_details"):
                st.session_state.view_mode = "list"
                st.session_state.selected_game = None
                st.rerun()

        st.subheader("Game Information")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Type:** {game.get('game_type', 'Not specified')}")
            st.write(f"**Difficulty:** {game.get('difficulty', 'Not specified')}")
        with col2:
            st.write(f"**Players:** {game.get('min_players', '-')} - {game.get('max_players', '-')}")
        with col3:
            st.write(f"**Duration:** {game.get('min_duration', '-')} min")

        st.subheader("Game Explanation")
        st.write(game.get('game_explanation', 'No explanation available.'))

        st.subheader("Materials Needed")
        materials = game.get('materials', [])
        if materials:
            if isinstance(materials, list):
                for material in materials:
                    st.write(f"- {material}")
            else:
                st.write(materials)
        else:
            st.write("No materials specified.")

        if game.get('rules'):
            st.subheader("Rules")
            st.write(game.get('rules'))

        if game.get('score_calculation'):
            st.subheader("Score Calculation")
            st.write(game.get('score_calculation'))

        if game.get('example'):
            st.subheader("Example")
            st.write(game.get('example'))

        expansions = game.get('expansions', [])
        if expansions and (isinstance(expansions, list) and len(expansions) > 0 or isinstance(expansions, str) and expansions.strip()):
            st.subheader("Expansions")
            if isinstance(expansions, list):
                for expansion in expansions:
                    st.write(f"- {expansion}")
            else:
                st.write(expansions)

        if game.get('drinking_rules'):
            with st.expander("Drinking Rules (21+ only)"):
                st.write(game.get('drinking_rules'))
