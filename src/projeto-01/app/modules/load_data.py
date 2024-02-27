from pathlib import Path

import pandas as pd
from pydantic import validate_call
from sqlalchemy import create_engine

from .config import create_connection_string_postgre


@validate_call
def read_csv_file(path: Path, delimiter: str) -> pd.DataFrame:
    "Realiza a leitura de arquivos CSV e coloca em um dataframe do pandas."
    try:
        if Path(path).is_file() == False:
            raise FileNotFoundError
        else:
            df = pd.read_csv(
                path, delimiter=delimiter, encoding="utf-8", header=0, index_col=False
            )
            return df
    except FileNotFoundError:
        print("O arquivo para carregamento não foi encontrado.")
        exit()
    except Exception as e:
        print(e)
        exit()


@validate_call
def load_table_postgre(df, table: str, mode: str, schema: str) -> None:
    "Realiza o carregamento da informação no banco PostgreSQL em modo de replace ou append."
    engine = create_engine(create_connection_string_postgre())
    df.to_sql(name=table, schema=schema, con=engine, if_exists=mode, index=False)
