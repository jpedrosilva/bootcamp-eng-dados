import pandas as pd
from pydantic import validate_call
from sqlalchemy import create_engine


@validate_call
def extract_data_pd(connection_string: str, query: str) -> pd.DataFrame:
    """Extrair os dados do banco PostgreSQL para um pandas dataframe"""
    try:
        # Cria a engine para conexão com o banco PostgreSQL
        engine = create_engine(connection_string)

        # Executa a query e armazena em um pandas dataframe
        with engine.connect() as conn, conn.begin():
            df = pd.read_sql_query(query, conn)

        return df

    except Exception as e:
        print(f"Erro ao extrair os dados do banco de dados.\nERROR: {e}")
