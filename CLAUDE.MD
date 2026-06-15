# CLAUDE.md

## Project Context

This project is a teaching demo for a Claude Code course.

The goal is to build a local Streamlit dashboard for the FIFA World Cup 2026 using Python, SQLite and an optional football API.

The project must help students understand:

* local development
* terminal workflow
* Python project structure
* SQLite databases
* Streamlit dashboards
* API integration
* spec-driven development
* planning before implementation

## Teaching Principles

This project is for beginners.

Always prioritize:

* simple code
* readable structure
* clear file names
* comments where useful
* step-by-step explanations
* local-first development

Avoid unnecessary complexity.

Do not introduce cloud services, authentication, Docker, advanced frontend frameworks or production deployment unless explicitly requested.

## Tech Stack

Use:

* Python
* Streamlit
* SQLite
* pandas
* requests
* python-dotenv

## Project Rules

Before writing code:

1. Read the relevant spec file from `specs/`
2. Create an implementation plan
3. Explain assumptions
4. Ask for approval before editing files

When implementing:

* Keep Streamlit UI simple
* Keep database logic separate from UI
* Keep API logic separate from database logic
* Use SQLite as the local source of truth
* Never hardcode API keys
* Use `.env` for secrets
* Provide `.env.example`
* Update README when commands change

## Architecture

Preferred file responsibilities:

* `app.py`: Streamlit interface
* `database.py`: SQLite connection and queries
* `seed.py`: creates and seeds the local database
* `api_client.py`: calls external football API
* `sync_matches.py`: syncs API data into SQLite
* `requirements.txt`: dependencies
* `.env.example`: environment variable template

## Important Learning Message

Claude Code is an AI coworker, not a replacement for the developer.

The developer should define the goal, review the plan, approve changes, test the result and understand the architecture.
