from pathlib import Path

import pandas as pd
from pydantic import validate_call
from sqlalchemy import create_engine
from tqdm import tqdm

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


def chuncker(seq, size):
    """Criação do chunker para controle da barra de progresso."""
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


@validate_call
def load_table_postgre(df, table: str, schema: str) -> None:
    "Realiza o carregamento da informação no banco PostgreSQL em modo de replace ou append."
    try:
        # Criação da engine
        engine = create_engine(create_connection_string_postgre())

        # Barra de progresso
        print(f"Carga da tabela {table} iniciada.")
        chunksize = int(len(df) / 10)
        with tqdm(total=len(df)) as pbar:
            for i, cdf in enumerate(chuncker(df, chunksize)):
                replace = "replace" if i == 0 else "append"
                cdf.to_sql(
                    name=table,
                    schema=schema,
                    con=engine,
                    if_exists=replace,
                    index=False,
                    method="multi",
                )
                pbar.update(chunksize)
        print(f"Carga finalizada com sucesso.")
    except Exception as e:
        print(f"Houve um erro ne execução da carga.\nERROR: {e}")
