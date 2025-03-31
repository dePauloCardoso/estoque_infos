from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from db_config import DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD

# 1. Estabelecer Conexão com o Banco de Dados usando SQLAlchemy
def connect_to_db():
    connection_string = (
        f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    engine = create_engine(connection_string)
    return engine

# 2. Executar Consultas SQL e Retornar DataFrame
def query_stock_to_dataframe(engine):
    query = """
    SELECT DISTINCT
        (B2_FILIAL) AS FILIAL,
        CASE 
            WHEN B2_FILIAL = '110102' THEN 'JDI'
            WHEN B2_FILIAL = '110104' THEN 'FOR'
        END AS UF_FILIAL,
        TRIM(B2_COD) AS PRODUTO,
        TRIM(B1_DESC) AS DESCRICAO,  
        B2_LOCAL AS ARMAZEM,
        BF_QUANT AS QUANTIDADE
    FROM SB2030 (NOLOCK)
    LEFT JOIN SBF030 (NOLOCK) ON BF_PRODUTO = B2_COD
                              AND BF_LOCAL = B2_LOCAL
                              AND BF_FILIAL = B2_FILIAL
    LEFT JOIN SB1030 (NOLOCK) ON B1_COD = B2_COD
    WHERE (1 = 1)
    AND SB2030.D_E_L_E_T_ = ''
    AND SBF030.D_E_L_E_T_ = ''
    AND B2_FILIAL IN ('110102', '110104')
    AND B2_LOCAL IN ('01')
    AND BF_LOCAL IN ('01')
    AND BF_QUANT <> '0'
    AND B2_QATU <> '0'
    ORDER BY PRODUTO
    """
    df = pd.read_sql_query(query, engine)
    return df

# 3. Fechar a Conexão
def close_connection(engine):
    engine.dispose()
