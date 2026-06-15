"""
Sincroniza partidas da API football-data.org com o banco SQLite local.
Partidas com manual_override=1 têm seus placares e status preservados.

Uso: python sync_matches.py
"""

from api_client import fetch_world_cup_matches
from database import init_db, upsert_match


def sync():
    init_db()

    print("Buscando partidas na API...")
    matches = fetch_world_cup_matches()

    if not matches:
        print("Nenhuma partida retornada. Verifique a API key ou conexão.")
        return

    print(f"{len(matches)} partidas recebidas. Atualizando banco...")

    counts = {"inserted": 0, "updated": 0, "skipped": 0}
    for match in matches:
        result = upsert_match(match)
        counts[result] += 1

    print(
        f"\nSincronização concluída:\n"
        f"  ✓ {counts['inserted']} inseridas\n"
        f"  ↻ {counts['updated']} atualizadas\n"
        f"  ⚑ {counts['skipped']} ignoradas (override manual ativo)"
    )


if __name__ == "__main__":
    sync()
