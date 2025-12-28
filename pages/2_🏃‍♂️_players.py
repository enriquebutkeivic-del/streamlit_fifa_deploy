import streamlit as st

st.set_page_config(
    page_title = "Players",
    page_icon = "🏃‍♂️",
    layout = "wide"
)

from io import BytesIO
import requests


df_data = st.session_state["data"]

## Construindo seletores no canto esquerdo - utilizando Siderbar

clubes = df_data["Club"].value_counts().index  ## todos os clubes disponiveis
club = st.sidebar.selectbox("Clube", clubes) ## clube selecionado

df_players = df_data[(df_data["Club"] == club)] ## Filtro
players = df_players["Name"].value_counts().index 
player = st.sidebar.selectbox("Jogador", players)

player_stats = df_data[df_data["Name"] == player].iloc[0]


@st.cache_data
def load_image(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    return BytesIO(r.content)

st.image(load_image(player_stats["Photo"]), width=70)



st.title(player_stats["Name"])

st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100}")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f}")
st.divider()

st.subheader(f"Overall{player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))


col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Valor de mercado", value = f"(£){player_stats['Value(£)']:,}")
col2.metric(label="Remuneração semanal", value = f"(£){player_stats['Wage(£)']:,}")
col3.metric(label="Cláusula de rescisão", value = f"(£){player_stats['Release Clause(£)']:,}")
