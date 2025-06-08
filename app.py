import streamlit as st
import requests
import datetime

st.set_page_config(page_title="VINITAG", layout="wide")

# 🌟 Neon CSS + Fonte Orbitron
st.markdown("""
<style>
body {
    background-color: #0f0f0f;
    color: #39ff14;
    font-family: 'Orbitron', sans-serif;
}
.neon {
    text-shadow:
      0 0 5px #39ff14,
      0 0 10px #39ff14,
      0 0 20px #39ff14,
      0 0 40px #39ff14;
    color: #39ff14;
}
.panel {
    background: rgba(255, 255, 255, 0.05);
    padding: 2em;
    border-radius: 20px;
    box-shadow: 0 0 20px #0ff;
    transform: perspective(600px) rotateY(5deg);
    margin-top: 2em;
}
</style>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 🌈 Título Neon 3D
st.markdown("<h1 class='neon'>⚡ VINITAG - Futebol em Tempo Real ⚽</h1>", unsafe_allow_html=True)

# 🔑 Chave da API
API_KEY = st.secrets["api_football_key"]
BASE_URL = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": API_KEY}

# 📝 Entrada do usuário
team_name = st.text_input("Digite o nome do time para buscar:", "Corinthians")

# 🔍 Busca os jogos
if st.button("Buscar Partidas"):
    with st.spinner("Buscando dados..."):
        team_res = requests.get(BASE_URL + "/teams", params={"search": team_name}, headers=headers)
        team_data = team_res.json().get("response", [])

        if team_data:
            team_id = team_data[0]["team"]["id"]
            name = team_data[0]["team"]["name"]
            logo = team_data[0]["team"]["logo"]

            st.markdown(f"<div class='panel'><img src='{logo}' width='80'><h2 class='neon'>{name}</h2>", unsafe_allow_html=True)

            # Últimos 10 dias
            today = datetime.date.today()
            last_10_days = today - datetime.timedelta(days=10)

            fixtures_res = requests.get(
                BASE_URL + "/fixtures",
                params={
                    "team": team_id,
                    "from": last_10_days,
                    "to": today,
                    "status": "FT",
                    "limit": 5
                },
                headers=headers
            )
            matches = fixtures_res.json().get("response", [])

            if matches:
                for match in matches:
                    date = match["fixture"]["date"][:10]
                    home = match["teams"]["home"]["name"]
                    away = match["teams"]["away"]["name"]
                    score = f"{match['goals']['home']} x {match['goals']['away']}"
                    st.markdown(f"<p class='neon'>{date}: <strong>{home}</strong> {score} <strong>{away}</strong></p>", unsafe_allow_html=True)
            else:
                st.warning("Sem partidas recentes encontradas.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Time não encontrado.")
