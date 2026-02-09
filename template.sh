#!/bin/bash

echo "Creating Doc_ai project structure..."

# Core folders
mkdir -p app data uploads vectorstore ui tests scripts

# App files
touch app/__init__.py
touch app/main.py
touch app/rag.py
touch app/extraction.py
touch app/guardrails.py
touch app/utils.py
touch app/config.py
touch app/prompts.py

# UI
touch ui/streamlit_app.py

# Root files
touch requirements.txt
touch README.md
touch .env
touch .gitignore

echo "Done"