# 🎬 Movies dataset template

A simple Streamlit app showing movie data from [The Movie Database (TMDB)](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movies-dataset-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### Structure
games-database/                  # Root project directory
│
├── streamlit_app.py            # Main Streamlit application file (replaces your current file)
├── firebase_config.py          # Firebase configuration and connection utilities
├── seed_data.py                # Optional utility to seed your database with sample data
│
├── .streamlit/                 # Streamlit configuration directory
│   └── secrets.toml            # Secret configuration for Firebase (do not commit this)
│
├── .devcontainer/              # Development container configuration (already exists)
│   └── devcontainer.json       # VS Code development container settings
│
├── data/                       # Data directory (you can keep this for any local data)
│   └── placeholder.md          # You can keep this as a placeholder
│
├── .gitignore                  # Git ignore file to exclude sensitive files
└── requirements.txt            # Project dependencies (update this)
