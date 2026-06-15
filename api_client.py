"""
Cliente para a API football-data.org.
Documentação: https://www.football-data.org/documentation/quickstart
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"
COMPETITION_CODE = "WC"

STATUS_MAP = {
    "SCHEDULED": "scheduled",
    "TIMED":     "scheduled",
    "IN_PLAY":   "live",
    "PAUSED":    "live",
    "LIVE":      "live",
    "FINISHED":  "finished",
    "CANCELLED": "scheduled",
    "POSTPONED": "scheduled",
}


def _get_headers():
    api_key = os.getenv("FOOTBALL_DATA_API_KEY")
    if not api_key:
        return None
    return {"X-Auth-Token": api_key}


def fetch_world_cup_matches():
    """
    Busca partidas da Copa do Mundo 2026 na API.
    Retorna lista de dicionários normalizados ou [] em caso de falha.
    """
    headers = _get_headers()
    if not headers:
        print("FOOTBALL_DATA_API_KEY não encontrada no .env — sincronização ignorada.")
        return []

    try:
        response = requests.get(
            f"{BASE_URL}/competitions/{COMPETITION_CODE}/matches",
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao conectar na API: {e}")
        return []

    data = response.json()
    matches = data.get("matches", [])

    return [_normalize(m) for m in matches if _normalize(m)]


def _normalize(m):
    try:
        full_time = m.get("score", {}).get("fullTime", {})
        return {
            "external_id": str(m["id"]),
            "date":        m.get("utcDate", "")[:10],
            "group_name":  _format_group(m.get("group")),
            "home_team":   m.get("homeTeam", {}).get("name", ""),
            "away_team":   m.get("awayTeam", {}).get("name", ""),
            "home_score":  full_time.get("home"),
            "away_score":  full_time.get("away"),
            "status":      STATUS_MAP.get(m.get("status", ""), "scheduled"),
            "stadium":     m.get("venue", ""),
            "city":        "",
        }
    except (KeyError, TypeError):
        return None


def _format_group(group_str):
    if not group_str:
        return ""
    # API returns "GROUP_A" → "Grupo A"
    return group_str.replace("GROUP_", "Grupo ")
