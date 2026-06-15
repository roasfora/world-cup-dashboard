import streamlit as st
import pandas as pd
from database import init_db, get_all_matches, update_match, reset_override, get_match_by_id

st.set_page_config(
    page_title="Copa do Mundo 2026",
    page_icon="⚽",
    layout="wide",
)

init_db()


# ─── Helpers ─────────────────────────────────────────────────────────────────

@st.cache_data(ttl=30)
def load_matches():
    return get_all_matches()


def invalidate_cache():
    load_matches.clear()


def score_display(home, away):
    if home is None or away is None:
        return "— : —"
    return f"{home} : {away}"


SOURCE_BADGE = {
    "api":    "🌐 API",
    "manual": "✏️ Manual",
    "seed":   "🌱 Seed",
}


# ─── Header ──────────────────────────────────────────────────────────────────

st.title("⚽ Copa do Mundo FIFA 2026")
st.caption("Dashboard de acompanhamento de partidas — dados locais via SQLite")

# ─── Métricas ────────────────────────────────────────────────────────────────

matches = load_matches()
df = pd.DataFrame(matches)

total      = len(df)
scheduled  = len(df[df["status"] == "scheduled"]) if total else 0
live       = len(df[df["status"] == "live"]) if total else 0
finished   = len(df[df["status"] == "finished"]) if total else 0
total_goals = int(
    df["home_score"].fillna(0).sum() + df["away_score"].fillna(0).sum()
) if total else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Partidas", total)
col2.metric("Agendadas",         scheduled)
col3.metric("Ao Vivo",           live)
col4.metric("Encerradas",        finished)
col5.metric("Total de Gols",     total_goals)

st.divider()

# ─── Filtros e Tabela ─────────────────────────────────────────────────────────

st.subheader("Partidas")

if total == 0:
    st.info("Nenhuma partida no banco. Execute `python seed.py` para popular os dados.")
    st.stop()

groups = sorted(df["group_name"].unique().tolist())
teams  = sorted(set(df["home_team"].tolist() + df["away_team"].tolist()))

fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    sel_group = st.selectbox("Grupo", ["Todos"] + groups)
with fcol2:
    sel_team = st.selectbox("Time", ["Todos"] + teams)
with fcol3:
    sel_status = st.selectbox("Status", ["Todos", "scheduled", "live", "finished"])

filtered = df.copy()
if sel_group != "Todos":
    filtered = filtered[filtered["group_name"] == sel_group]
if sel_team != "Todos":
    filtered = filtered[(filtered["home_team"] == sel_team) | (filtered["away_team"] == sel_team)]
if sel_status != "Todos":
    filtered = filtered[filtered["status"] == sel_status]

display = filtered[["date", "group_name", "home_team", "home_score", "away_score", "away_team", "status", "data_source", "manual_override"]].copy()
display["placar"] = display.apply(lambda r: score_display(r["home_score"], r["away_score"]), axis=1)
display["fonte"]  = display["data_source"].map(SOURCE_BADGE).fillna(display["data_source"])
display["override"] = display["manual_override"].apply(lambda x: "⚑" if x == 1 else "")

st.dataframe(
    display[["date", "group_name", "home_team", "placar", "away_team", "status", "fonte", "override"]].rename(columns={
        "date":       "Data",
        "group_name": "Grupo",
        "home_team":  "Mandante",
        "away_team":  "Visitante",
        "status":     "Status",
        "fonte":      "Fonte",
        "override":   "Override",
    }),
    use_container_width=True,
    hide_index=True,
)

st.caption(f"{len(filtered)} de {total} partidas exibidas")

st.divider()

# ─── Administração de Partidas ────────────────────────────────────────────────

st.subheader("⚙️ Administração de Partidas")
st.caption("Edite placares manualmente. O override protege os dados durante a sincronização com a API.")


@st.fragment
def admin_panel():
    match_options = {
        f"[{r['group_name']}] {r['home_team']} × {r['away_team']} ({r['date']})": r["id"]
        for _, r in df.iterrows()
    }

    selected_label = st.selectbox("Selecione uma partida", list(match_options.keys()))
    match_id = match_options[selected_label]
    match = get_match_by_id(match_id)

    if not match:
        st.error("Partida não encontrada.")
        return

    badge = SOURCE_BADGE.get(match["data_source"], match["data_source"])
    override_flag = " — ⚑ Override ativo" if match["manual_override"] else ""
    st.info(f"Fonte atual: **{badge}**{override_flag}")

    with st.form("edit_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            home_score = st.number_input(
                f"Gols {match['home_team']}",
                min_value=0,
                value=int(match["home_score"]) if match["home_score"] is not None else 0,
                step=1,
            )
        with c2:
            away_score = st.number_input(
                f"Gols {match['away_team']}",
                min_value=0,
                value=int(match["away_score"]) if match["away_score"] is not None else 0,
                step=1,
            )
        with c3:
            status = st.selectbox(
                "Status",
                ["scheduled", "live", "finished"],
                index=["scheduled", "live", "finished"].index(match["status"]) if match["status"] in ["scheduled", "live", "finished"] else 0,
            )

        # Validação: alerta se encerrada sem placar
        if status == "finished" and (home_score is None or away_score is None):
            st.warning("Partidas encerradas devem ter placar preenchido.")

        save = st.form_submit_button("💾 Salvar", type="primary")

    if save:
        update_match(match_id, home_score, away_score, status)
        invalidate_cache()
        st.success("Resultado salvo com override manual ativo.")
        st.rerun()

    if match["manual_override"] == 1:
        if st.button("↩️ Resetar Override", help="Remove o override — próxima sincronização poderá sobrescrever este resultado"):
            reset_override(match_id)
            invalidate_cache()
            st.success("Override removido.")
            st.rerun()


admin_panel()
