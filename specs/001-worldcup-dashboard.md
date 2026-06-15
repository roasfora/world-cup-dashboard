# Spec 001 — World Cup 2026 Local Streamlit Dashboard

## Goal

Build a local Streamlit dashboard to visualize FIFA World Cup 2026 matches using a local SQLite database.

The app should work locally without requiring deploy or cloud infrastructure.

## Users

This app is for students learning:

* Python
* Streamlit
* SQLite
* APIs
* Claude Code
* spec-driven development

## Core Requirements

The app must:

1. Run locally with Streamlit
2. Store match data in SQLite
3. Show all matches in a table
4. Allow filtering by:

   * group
   * team
   * match status
5. Show simple metrics:

   * total matches
   * scheduled matches
   * finished matches
   * total goals
6. Allow manual editing of match results for games that do not yet have score information
7. Keep API data and manual updates clearly distinguishable
8. Work even if no API key is configured

## Non-Goals

This version must not include:

* user authentication
* remote database
* Vercel deploy
* Docker
* complex frontend
* advanced visual design
* real-time live match updates

## Data Model

Create a SQLite table called `matches`.

Columns:

* `id` INTEGER PRIMARY KEY AUTOINCREMENT
* `external_id` TEXT
* `date` TEXT
* `group_name` TEXT
* `home_team` TEXT
* `away_team` TEXT
* `home_score` INTEGER NULL
* `away_score` INTEGER NULL
* `status` TEXT
* `stadium` TEXT
* `city` TEXT
* `data_source` TEXT
* `last_updated` TEXT
* `manual_override` INTEGER DEFAULT 0

## Status Values

Use these status values:

* `scheduled`
* `live`
* `finished`

## Manual Result Editing

The app must allow the instructor or student to manually update:

* home score
* away score
* status

When a result is manually edited:

* set `manual_override = 1`
* set `data_source = "manual"`
* update `last_updated`

## Acceptance Criteria

The project is complete when:

1. `streamlit run app.py` opens the dashboard
2. The app loads matches from SQLite
3. Filters work correctly
4. Metrics update based on filters
5. Scheduled matches show no score
6. Finished matches show scores
7. A user can manually insert or update a result
8. Manual results persist after restarting the app
9. README explains how to setup and run the project
10. API key is optional
