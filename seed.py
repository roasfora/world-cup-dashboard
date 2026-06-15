"""
Populates worldcup.db with FIFA World Cup 2026 group stage matches.
Run once: python seed.py
"""

from database import init_db, has_data, get_connection
from datetime import timezone, datetime

MATCHES = [
    # Group A — USA, Panama, Bolivia
    ("A", "2026-06-11", "USA",     "Bolivia",  "SoFi Stadium",       "Los Angeles",    2, 0, "finished"),
    ("A", "2026-06-14", "Panama",  "Bolivia",  "Rose Bowl",          "Los Angeles",    1, 1, "finished"),
    ("A", "2026-06-19", "USA",     "Panama",   "SoFi Stadium",       "Los Angeles",    None, None, "scheduled"),

    # Group B — Mexico, Jamaica, Venezuela
    ("B", "2026-06-12", "Mexico",  "Venezuela","Estadio Azteca",      "Mexico City",   2, 1, "finished"),
    ("B", "2026-06-15", "Jamaica", "Venezuela","AT&T Stadium",        "Dallas",        0, 0, "finished"),
    ("B", "2026-06-20", "Mexico",  "Jamaica",  "Estadio Azteca",      "Mexico City",   None, None, "scheduled"),

    # Group C — Canada, Honduras, Morocco
    ("C", "2026-06-12", "Canada",  "Morocco",  "BC Place",            "Vancouver",     1, 0, "finished"),
    ("C", "2026-06-15", "Honduras","Morocco",  "Levi's Stadium",      "San Francisco", 0, 2, "finished"),
    ("C", "2026-06-20", "Canada",  "Honduras", "BC Place",            "Vancouver",     None, None, "scheduled"),

    # Group D — Argentina, Chile, Peru
    ("D", "2026-06-13", "Argentina","Peru",    "MetLife Stadium",     "New York",      3, 0, "finished"),
    ("D", "2026-06-13", "Chile",   "Peru",     "Hard Rock Stadium",   "Miami",         1, 0, "finished"),
    ("D", "2026-06-21", "Argentina","Chile",   "MetLife Stadium",     "New York",      None, None, "scheduled"),

    # Group E — Spain, Brazil, Japan
    ("E", "2026-06-14", "Spain",   "Japan",    "AT&T Stadium",        "Dallas",        2, 1, "finished"),
    ("E", "2026-06-14", "Brazil",  "Japan",    "NRG Stadium",         "Houston",       3, 0, "finished"),
    ("E", "2026-06-22", "Spain",   "Brazil",   "AT&T Stadium",        "Dallas",        None, None, "scheduled"),

    # Group F — England, France, Switzerland
    ("F", "2026-06-13", "England", "Switzerland","Levi's Stadium",    "San Francisco", 1, 1, "finished"),
    ("F", "2026-06-16", "France",  "Switzerland","Mercedes-Benz",     "Atlanta",       2, 0, "scheduled"),
    ("F", "2026-06-22", "England", "France",   "Levi's Stadium",      "San Francisco", None, None, "scheduled"),

    # Group G — Germany, Netherlands, Scotland
    ("G", "2026-06-15", "Germany", "Scotland", "Lincoln Financial",   "Philadelphia",  4, 1, "scheduled"),
    ("G", "2026-06-16", "Netherlands","Scotland","Empower Field",     "Denver",        None, None, "scheduled"),
    ("G", "2026-06-23", "Germany", "Netherlands","Lincoln Financial", "Philadelphia",  None, None, "scheduled"),

    # Group H — Portugal, Turkey, Czech Republic
    ("H", "2026-06-15", "Portugal","Czech Republic","Allegiant Stadium","Las Vegas",   None, None, "scheduled"),
    ("H", "2026-06-16", "Turkey",  "Czech Republic","State Farm",     "Phoenix",       None, None, "scheduled"),
    ("H", "2026-06-23", "Portugal","Turkey",   "Allegiant Stadium",   "Las Vegas",     None, None, "scheduled"),

    # Group I — Colombia, Ecuador, Costa Rica
    ("I", "2026-06-16", "Colombia","Costa Rica","MetLife Stadium",    "New York",      None, None, "scheduled"),
    ("I", "2026-06-17", "Ecuador", "Costa Rica","NRG Stadium",        "Houston",       None, None, "scheduled"),
    ("I", "2026-06-24", "Colombia","Ecuador",  "MetLife Stadium",     "New York",      None, None, "scheduled"),

    # Group J — Uruguay, South Korea, Qatar
    ("J", "2026-06-17", "Uruguay", "Qatar",    "Hard Rock Stadium",   "Miami",         None, None, "scheduled"),
    ("J", "2026-06-17", "South Korea","Qatar", "SoFi Stadium",        "Los Angeles",   None, None, "scheduled"),
    ("J", "2026-06-24", "Uruguay", "South Korea","Hard Rock Stadium", "Miami",         None, None, "scheduled"),

    # Group K — Belgium, Australia, Paraguay
    ("K", "2026-06-18", "Belgium", "Paraguay", "Mercedes-Benz",       "Atlanta",       None, None, "scheduled"),
    ("K", "2026-06-18", "Australia","Paraguay","AT&T Stadium",        "Dallas",        None, None, "scheduled"),
    ("K", "2026-06-25", "Belgium", "Australia","Mercedes-Benz",       "Atlanta",       None, None, "scheduled"),

    # Group L — Iran, New Zealand, Cameroon
    ("L", "2026-06-18", "Iran",    "Cameroon", "BC Place",            "Vancouver",     None, None, "scheduled"),
    ("L", "2026-06-19", "New Zealand","Cameroon","Estadio Azteca",    "Mexico City",   None, None, "scheduled"),
    ("L", "2026-06-25", "Iran",    "New Zealand","BC Place",          "Vancouver",     None, None, "scheduled"),

    # Group M — Senegal, Poland, Ukraine
    ("M", "2026-06-19", "Senegal", "Ukraine",  "Empower Field",       "Denver",        None, None, "scheduled"),
    ("M", "2026-06-19", "Poland",  "Ukraine",  "Allegiant Stadium",   "Las Vegas",     None, None, "scheduled"),
    ("M", "2026-06-26", "Senegal", "Poland",   "Empower Field",       "Denver",        None, None, "scheduled"),

    # Group N — Croatia, Ghana, Algeria
    ("N", "2026-06-20", "Croatia", "Algeria",  "Lincoln Financial",   "Philadelphia",  None, None, "scheduled"),
    ("N", "2026-06-20", "Ghana",   "Algeria",  "State Farm",          "Phoenix",       None, None, "scheduled"),
    ("N", "2026-06-26", "Croatia", "Ghana",    "Lincoln Financial",   "Philadelphia",  None, None, "scheduled"),

    # Group O — Nigeria, Egypt, Serbia
    ("O", "2026-06-21", "Nigeria", "Serbia",   "NRG Stadium",         "Houston",       None, None, "scheduled"),
    ("O", "2026-06-21", "Egypt",   "Serbia",   "Rose Bowl",           "Los Angeles",   None, None, "scheduled"),
    ("O", "2026-06-27", "Nigeria", "Egypt",    "NRG Stadium",         "Houston",       None, None, "scheduled"),

    # Group P — Saudi Arabia, Denmark, South Africa
    ("P", "2026-06-22", "Saudi Arabia","South Africa","State Farm",   "Phoenix",       None, None, "scheduled"),
    ("P", "2026-06-22", "Denmark", "South Africa","Levi's Stadium",   "San Francisco", None, None, "scheduled"),
    ("P", "2026-06-27", "Saudi Arabia","Denmark","State Farm",        "Phoenix",       None, None, "scheduled"),
]


def seed():
    init_db()

    if has_data():
        print("Banco já contém dados. Seed ignorado. Use --force para re-popular.")
        return

    now = datetime.now(timezone.utc).isoformat()
    with get_connection() as conn:
        for i, (group, date, home, away, stadium, city, h_score, a_score, status) in enumerate(MATCHES):
            conn.execute(
                """
                INSERT INTO matches
                    (external_id, date, group_name, home_team, away_team,
                     home_score, away_score, status, stadium, city, data_source, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'seed', ?)
                """,
                (f"seed-{i+1:03d}", date, f"Grupo {group}", home, away,
                 h_score, a_score, status, stadium, city, now),
            )

    total = len(MATCHES)
    print(f"✓ {total} partidas inseridas com sucesso.")


if __name__ == "__main__":
    import sys
    if "--force" in sys.argv:
        with get_connection() as conn:
            conn.execute("DELETE FROM matches")
        print("Dados anteriores removidos.")
    seed()
