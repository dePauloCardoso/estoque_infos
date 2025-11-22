import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# ====================== CARREGAMENTO DE DADOS ======================
@st.cache_data
def load_data_ppg_2025():
    return pd.read_csv("data/ppg_sae_2025.csv", sep=';')

@st.cache_data
def load_data_ppg_2026():
    return pd.read_csv("data/ppg_sae_2026.csv", sep=';')

df_ppg_2025 = load_data_ppg_2025()
df_ppg_2026 = load_data_ppg_2026()

# ====================== ESTILO ======================
st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #161B33;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image("https://github.com/dePauloCardoso/streamlit_app/blob/main/Logo_SAE.png?raw=true")

# ====================== MAPA DE SÉRIES ======================
serie_map = {
    "INF": ["", "INF I", "INF II", "INF III", "INF IV", "INF V"],
    "FUND AI": ["", "1O ANO", "2O ANO", "3O ANO", "4O ANO", "5O ANO"],
    "FUND AF": ["", "6O ANO", "7O ANO", "8O ANO", "9O ANO"],
    "EM": ["", "1A SERIE", "2A SERIE", "3A SERIE"],
    "PV": ["", "APROVA +", "ELETIVAS", "SEMI"],
    "VÁRIOS": ["", "VARIOS"]
}

# ====================== ABAS ======================
aba_2025, aba_2026 = st.tabs(["PPG-2025", "PPG-2026"])

# ============================
#         ABA 2025
# ============================
with aba_2025:
    st.sidebar.title("Filtros PPG-2025")

    cod_insersao_25 = st.sidebar.text_input("Código de Inserção", key="ci25")
    cod_sku_25 = st.sidebar.text_input("Código SKU", key="sku25")

    segmento_25 = st.sidebar.selectbox(
        "Segmento",
        ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"],
        key="seg25"
    )

    serie_25 = st.sidebar.selectbox(
        "Série",
        serie_map.get(segmento_25, [""]),
        key="ser25"
    )

    envio_25 = st.sidebar.selectbox("", ["", "V1", "V2", "V3", "V4"], key="env25")
    usuario_25 = st.sidebar.selectbox("Usuário", ["", "Aluno", "Professor"], key="usu25")

    personalizacao_25 = st.sidebar.selectbox(
        "Personalização",
        ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER", "DOM BOSCO", "DOM BOSCO BALSAS",
         "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR",
         "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE",
         "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"],
        key="pers25"
    )

    # ---- FILTRO ----
    filtro = pd.Series([True] * len(df_ppg_2025))

    if cod_insersao_25:
        filtro &= df_ppg_2025['cod_insersao'].astype(str).str.contains(cod_insersao_25, na=False)
    if cod_sku_25:
        filtro &= df_ppg_2025['cod_sku'].astype(str).str.contains(cod_sku_25, na=False)
    if segmento_25:
        filtro &= df_ppg_2025['segmento'] == segmento_25
    if serie_25:
        filtro &= df_ppg_2025['serie'] == serie_25
    if envio_25:
        filtro &= df_ppg_2025['envio'] == envio_25
    if usuario_25:
        filtro &= df_ppg_2025['usuario'] == usuario_25
    if personalizacao_25:
        filtro &= df_ppg_2025['personalizacao'] == personalizacao_25

    df_exibir_25 = df_ppg_2025[filtro]

    if not df_exibir_25.empty:
        st.dataframe(df_exibir_25, use_container_width=True)
    else:
        st.warning("Nenhum produto encontrado para estes filtros.")


# ============================
#         ABA 2026
# ============================
with aba_2026:
    st.sidebar.title("Filtros PPG-2026")

    cod_insersao_26 = st.sidebar.text_input("Código de Inserção", key="ci26")
    cod_sku_26 = st.sidebar.text_input("Código SKU", key="sku26")

    segmento_26 = st.sidebar.selectbox(
        "Segmento",
        ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"],
        key="seg26"
    )

    serie_26 = st.sidebar.selectbox(
        "Série",
        serie_map.get(segmento_26, [""]),
        key="ser26"
    )

    usuario_26 = st.sidebar.selectbox("Usuário", ["", "Aluno", "Professor"], key="usu26")

    # envio_26 = st.sidebar.selectbox("Envio", ["", "V1", "V2", "V3", "V4"], key="env26")

    # ---- FILTRO ----
    filtro = pd.Series([True] * len(df_ppg_2026))

    if cod_insersao_26:
        filtro &= df_ppg_2026['cod_insersao'].astype(str).str.contains(cod_insersao_26, na=False)
    if cod_sku_26:
        filtro &= df_ppg_2026['cod_sku'].astype(str).str.contains(cod_sku_26, na=False)
    if segmento_26:
        filtro &= df_ppg_2026['segmento'] == segmento_26
    if serie_26:
        filtro &= df_ppg_2026['serie'] == serie_26
    if usuario_26:
        filtro &= df_ppg_2026['usuario'] == usuario_26

    df_exibir_26 = df_ppg_2026[filtro]

    if not df_exibir_26.empty:
        st.dataframe(df_exibir_26, use_container_width=True)
    else:
        st.warning("Nenhum produto encontrado para estes filtros.")


# ====================== LIMPAR FILTROS ======================
def limpar_filtros():
    for key in list(st.session_state.keys()):
        st.session_state[key] = ""

st.sidebar.button("Limpar Filtros", on_click=limpar_filtros)
