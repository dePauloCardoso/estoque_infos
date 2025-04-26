import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Carrega os dados de PPG
@st.cache_data
def load_data_ppg():
    return pd.read_csv("data/ppg_sae_2025.csv", sep=';')

# Carrega os dados de Estoque do Google Sheets
@st.cache_data
def load_data_estoque(url):
    try:
        csv_export_url = url.replace('/pubhtml', '/pub?output=csv')
        return pd.read_csv(csv_export_url)
    except Exception as e:
        st.error(f"Erro ao carregar dados do Google Sheets: {e}")
        return pd.DataFrame()

# Carrega os dados de Contratos
@st.cache_data
def load_data_contratos():
    return pd.read_csv("data/contratosSae.csv", sep=';') # Adaptar com seu arquivo

# Define o link do Google Sheets para o Estoque
SHEETS_URL_ESTOQUE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVpYelrsyO0cuBSQxwvaT8SkTdyrnzOvbPHWZLamz4MrWCKsZ733e_hKfe45bgqFpX0YIj2ohmrssn/pubhtml"

# # Carrega os DataFrames
# df_ppg = load_data_ppg()
# df_estoque = load_data_estoque(SHEETS_URL_ESTOQUE)
# df_contratos = load_data_contratos()

# Carrega os DataFrames
df_ppg = load_data_ppg()
df_estoque = load_data_estoque(SHEETS_URL_ESTOQUE)
print("Colunas do df_estoque:", df_estoque.columns) # Adicione esta linha para inspeção
df_contratos = load_data_contratos()

# Define a cor de fundo
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

# Exibe a imagem
st.sidebar.image("https://github.com/dePauloCardoso/streamlit_app/blob/main/Logo_SAE.png?raw=true")

# Inicializa os filtros no session_state
if "segmento" not in st.session_state:
    st.session_state.segmento = ""
if "serie" not in st.session_state:
    st.session_state.serie = ""
if "cod_insersao" not in st.session_state:
    st.session_state.cod_insersao = ""
if "cod_sku" not in st.session_state:
    st.session_state.cod_sku = ""
if "envio" not in st.session_state:
    st.session_state.envio = ""
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "personalizacao" not in st.session_state:
    st.session_state.personalizacao = ""
if "filial" not in st.session_state:
    st.session_state.filial = ""
if "uf_filial" not in st.session_state:
    st.session_state.uf_filial = ""
if "produto_estoque" not in st.session_state:
    st.session_state.produto_estoque = ""
if "zz1_client" not in st.session_state:
    st.session_state.zz1_client = ""
if "zz1_numero" not in st.session_state:
    st.session_state.zz1_numero = ""
if "zz1_produt" not in st.session_state:
    st.session_state.zz1_produt = ""

# Mapeamento de Série baseado no Segmento
serie_map = {
    "INF": ["", "INF I", "INF II", "INF III", "INF IV", "INF V"],
    "FUND AI": ["", "1O ANO", "2O ANO", "3O ANO", "4O ANO", "5O ANO"],
    "FUND AF": ["", "6O ANO", "7O ANO", "8O ANO", "9O ANO"],
    "EM": ["", "1A SERIE", "2A SERIE", "3A SERIE"],
    "PV": ["", "APROVA +", "ELETIVAS", "SEMI"],
    "VÁRIOS": ["", "VARIOS"]
}

# Cria as abas
aba_ppg, aba_estoque, aba_contratos = st.tabs(["PPG", "Estoque", "Contratos"])

# Conteúdo da aba PPG
with aba_ppg:
    st.sidebar.title("Consulta de Produtos")
    st.session_state.cod_insersao = st.sidebar.text_input("Código de Inserção", st.session_state.cod_insersao)
    st.session_state.cod_sku = st.sidebar.text_input("Código SKU", st.session_state.cod_sku)
    segmento_options = ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"]
    st.session_state.segmento = st.sidebar.selectbox("Segmento", segmento_options, index=segmento_options.index(st.session_state.segmento))
    serie_options = serie_map.get(st.session_state.segmento, [""])
    st.session_state.serie = st.sidebar.selectbox("Série", serie_options, index=serie_options.index(st.session_state.serie) if st.session_state.serie in serie_options else 0)
    envio_options = ["", "V1", "V2", "V3", "V4"]
    st.session_state.envio = st.sidebar.selectbox("Envio", envio_options, index=envio_options.index(st.session_state.envio))
    usuario_options = ["", "Aluno", "Professor"]
    st.session_state.usuario = st.sidebar.selectbox("Usuário", usuario_options, index=usuario_options.index(st.session_state.usuario))
    personalizacao_options = ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER", "DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"]
    st.session_state.personalizacao = st.sidebar.selectbox("Personalização", personalizacao_options, index=personalizacao_options.index(st.session_state.personalizacao))

    filtro_ppg = pd.Series([True] * len(df_ppg))
    if st.session_state.cod_insersao:
        filtro_ppg &= df_ppg['cod_insersao'].astype(str).str.contains(st.session_state.cod_insersao, na=False)
    if st.session_state.cod_sku:
        filtro_ppg &= df_ppg['cod_sku'].astype(str).str.contains(st.session_state.cod_sku, na=False)
    if st.session_state.segmento:
        filtro_ppg &= df_ppg['segmento'] == st.session_state.segmento
    if st.session_state.serie:
        filtro_ppg &= df_ppg['serie'] == st.session_state.serie
    if st.session_state.envio:
        filtro_ppg &= df_ppg['envio'] == st.session_state.envio
    if st.session_state.usuario:
        filtro_ppg &= df_ppg['usuario'] == st.session_state.usuario
    if st.session_state.personalizacao:
        filtro_ppg &= df_ppg['personalizacao'] == st.session_state.personalizacao

    df_filtrado_ppg = df_ppg[filtro_ppg]
    if not df_filtrado_ppg.empty:
        colunas_desejadas = ['cod_insersao', 'descricao_kit', 'cod_sku', 'descricao_sku', 'segmento', 'serie', 'volume', 'envio', 'frequencia', 'usuario', 'info_produto', 'tipo_material', 'classificacao_produto', 'personalizacao']
        df_filtrado_ppg = df_filtrado_ppg[colunas_desejadas]
        st.dataframe(df_filtrado_ppg, use_container_width=True)
    else:
        st.write("Nenhum produto encontrado para estes filtros.")

# Conteúdo da aba Estoque
with aba_estoque:
    st.sidebar.title("Filtros de Estoque")
    filial_options = [""] + list(df_estoque['FILIAL'].unique().astype(str))
    st.session_state.filial = st.sidebar.selectbox("Filial", filial_options, index=filial_options.index(st.session_state.filial) if st.session_state.filial in filial_options else 0)
    uf_filial_options = [""] + list(df_estoque['UF_FILIAL'].unique())
    st.session_state.uf_filial = st.sidebar.selectbox("UF_FILIAL", uf_filial_options, index=uf_filial_options.index(st.session_state.uf_filial) if st.session_state.uf_filial in uf_filial_options else 0)
    st.session_state.produto_estoque = st.sidebar.text_input("Produto", st.session_state.produto_estoque)

    filtro_estoque = pd.Series([True] * len(df_estoque))
    if st.session_state.filial:
        filtro_estoque &= df_estoque['FILIAL'].astype(str) == st.session_state.filial
    if st.session_state.uf_filial:
        filtro_estoque &= df_estoque['UF_FILIAL'] == st.session_state.uf_filial
    if st.session_state.produto_estoque:
        filtro_estoque &= df_estoque['PRODUTO'].astype(str).str.contains(st.session_state.produto_estoque, na=False)

    df_filtrado_estoque = df_estoque[filtro_estoque]
    if not df_filtrado_estoque.empty:
        st.dataframe(df_filtrado_estoque, use_container_width=True)
    else:
        st.write("Nenhum item de estoque encontrado para estes filtros.")

# Conteúdo da aba Contratos
with aba_contratos:
    st.sidebar.title("Filtros de Contratos")
    st.session_state.zz1_client = st.sidebar.text_input("Cliente", st.session_state.zz1_client)
    st.session_state.zz1_numero = st.sidebar.text_input("Número", st.session_state.zz1_numero)
    st.session_state.zz1_produt = st.sidebar.text_input("Código", st.session_state.zz1_produt)

    filtro_contratos = pd.Series([True] * len(df_contratos))
    if st.session_state.zz1_client:
        filtro_contratos &= df_contratos['ZZ1_CLIENT'].astype(str).str.contains(st.session_state.zz1_client, na=False)
    if st.session_state.zz1_numero:
        filtro_contratos &= df_contratos['ZZ1_NUMERO'].astype(str).str.contains(st.session_state.zz1_numero, na=False)
    if st.session_state.zz1_produt:
        filtro_contratos &= df_contratos['ZZ1_PRODUT'].astype(str).str.contains(st.session_state.zz1_produt, na=False)

    df_filtrado_contratos = df_contratos[filtro_contratos]
    if not df_filtrado_contratos.empty:
        st.dataframe(df_filtrado_contratos, use_container_width=True)
    else:
        st.write("Nenhum contrato encontrado para estes filtros.")

# Botão Limpar Filtros (fora das abas para aplicar a todas)
def limpar_filtros():
    for key in st.session_state.keys():
        st.session_state[key] = ""

st.sidebar.button("Limpar Filtros", on_click=limpar_filtros)