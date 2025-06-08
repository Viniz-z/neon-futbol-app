import streamlit as st import requests import datetime from streamlit_autorefresh import st_autorefresh

Configuração da página

st.set_page_config(page_title="VINITAG", layout="wide")

Neon CSS

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
    font-size: 3em;
    text-align: center;
    margin-top: 0.5em;
}
.panel {
    background: rgba(255, 255, 255, 0.05);
    padding: 2em;
    border-radius: 20px;
    box-shadow: 0 0 20px #0ff;
    margin-top: 2em;
}
</style><link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)Título 3D Neon

st.markdown("""

<h1 class='neon'>🔥 VINITAG - Partidas AO VIVO 🔥</h1>
""", unsafe_allow_html=True)Atualiza a cada 30 segundos

st_autorefresh(interval=30 * 1000, key="live_data_refresh")

API

API_KEY = st.secrets["api_football_key"] BASE_URL = "https://v3.football.api-sports.io" headers = {"x-apisports-key": API_KEY}

Buscar jogos ao vivo

with st.spinner("Buscando jogos ao vivo..."): res = requests.get(BASE_URL + "/fixtures", params={"live": "all"}, headers=headers) matches = res.json().get("response", [])

if matches: for match in matches: fixture = match["fixture"] league = match["league"]["name"] home = match["teams"]["home"] away = match["teams"]["away"] goals = match["goals"] status = fixture["status"]["elapsed"]

st.markdown(f"""
    <div class='panel'>
        <h3 class='neon'>{league}</h3>
        <p class='neon'>⏱ {status}' - <strong>{home['name']}</strong> {goals['home']} x {goals['away']} <strong>{away['name']}</strong></p>
    </div>
    """, unsafe_allow_html=True)

else: st.warning("Nenhuma partida ao vivo neste momento.")

