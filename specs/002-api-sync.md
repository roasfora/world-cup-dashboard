# Spec 002 — API Sync for World Cup Match Data

## Goal

Add optional API synchronization to fetch FIFA World Cup 2026 matches and results from a football data API.

The local SQLite database remains the source of truth for the Streamlit app.

## Recommended API

Use `football-data.org` as the first implementation option.

API key must be stored in `.env`:

FOOTBALL_DATA_API_KEY=your_api_key_here

## Requirements

The sync must:

1. Read API key from `.env`
2. Fetch World Cup 2026 match data when available
3. Normalize API data into the local `matches` table
4. Insert new matches
5. Update existing matches
6. Preserve manual overrides
7. Never overwrite manually edited results unless explicitly requested

## Manual Override Rule

If `manual_override = 1`, the sync should not overwrite:

* `home_score`
* `away_score`
* `status`

It may update metadata such as:

* stadium
* city
* external_id
* last_updated

## Fallback Behavior

If API key is missing or the API request fails:

* app should continue working
* show a clear warning in Streamlit
* keep using local SQLite data

## Acceptance Criteria

The feature is complete when:

1. `python sync_matches.py` fetches data from the API
2. API data is saved into SQLite
3. Manual results are not overwritten
4. Missing API key does not break the app
5. README explains API setup
6. `.env.example` includes the required variable
