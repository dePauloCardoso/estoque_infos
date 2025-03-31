from db_extract import connect_to_db, query_stock_to_dataframe, close_connection

def main():
    # Estabelecer Conexão
    conn = connect_to_db()
    try:
        # Consulta de Estoque
        estoque_df = query_stock_to_dataframe(conn)
        estoque_path = 'data/estoqueSae.csv'
        estoque_df.to_csv(estoque_path, index=False)

    except Exception as e:
        print(f"Erro ao executar a consulta ou salvar o arquivo: {e}")
    
    finally:
        # Fechar Conexão
        close_connection(conn)

if __name__ == "__main__":
    main()
