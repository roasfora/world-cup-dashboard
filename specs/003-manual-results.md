# Spec 003 — Manual Result Management

## Goal

Allow instructors and students to manually create, edit and override World Cup 2026 match results from the Streamlit interface.

This feature demonstrates the concept of Human-in-the-Loop systems where human decisions can override automated data sources.

The local SQLite database remains the source of truth.

---

## Business Context

External APIs may:

* be unavailable
* contain incorrect information
* have delayed updates
* not yet contain future match results

Users must be able to manually maintain match information.

---

## User Stories

### Story 1

As a user

I want to manually enter the result of a match

So that I can update games before the API has official data.

---

### Story 2

As a user

I want to edit an existing result

So that I can correct mistakes.

---

### Story 3

As a user

I want to know whether a result came from the API or was manually entered

So that I understand the source of the data.

---

### Story 4

As a user

I want manual changes to persist

So that my changes are not lost when the application restarts.

---

## Functional Requirements

### View Match Details

The application must allow selecting a match.

Display:

* Home team
* Away team
* Date
* Group
* Current status
* Current score
* Data source

---

### Edit Match Result

The user must be able to edit:

* Home score
* Away score
* Status

Allowed statuses:

* scheduled
* live
* finished

---

### Save Changes

When the user saves:

Update:

* home_score
* away_score
* status
* last_updated

Set:

* manual_override = 1
* data_source = "manual"

---

### Create Future Predictions

For matches that have not yet occurred:

The user may manually enter a predicted score.

Example:

Brazil 3 x 1 Morocco

The application should allow storing these predictions.

---

### Reset Override

The application must allow resetting manual changes.

When reset:

* manual_override = 0

The next synchronization may overwrite the match using API data.

---

## Data Source Transparency

Every match must display its source.

Possible values:

* api
* manual
* seed

Example:

Mexico 2 x 0 South Africa

Source: API

---

Example:

Brazil 3 x 1 Morocco

Source: Manual Override

---

## Database Changes

The matches table must include:

manual_override INTEGER DEFAULT 0

data_source TEXT

last_updated TEXT

---

## Streamlit Interface

Create a section called:

Match Administration

Features:

* Select match
* Edit scores
* Edit status
* Save changes
* Reset override

Display success messages after updates.

---

## Validation Rules

Scores cannot be negative.

Scheduled matches may have null scores.

Finished matches should contain scores.

The application should warn when:

* status is finished
* score is missing

---

## Human-in-the-Loop Concept

This feature exists for educational purposes.

The project should demonstrate:

API Data
↓
Local Database
↓
Human Review
↓
Manual Override
↓
Final Result

The human remains responsible for approving and correcting data.

---

## Acceptance Criteria

The feature is complete when:

1. A user can edit a match result from Streamlit.
2. Changes persist in SQLite.
3. Manual edits survive application restarts.
4. API synchronization does not overwrite manual changes.
5. Users can identify the source of each result.
6. Users can reset an override.
7. Validation prevents invalid scores.
8. The UI clearly communicates when a result is manually controlled.
