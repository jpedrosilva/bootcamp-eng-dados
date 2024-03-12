from pathlib import Path

import pandas as pd
from pydantic import validate_call
from sqlalchemy import create_engine
from tqdm import tqdm

from .config import create_connection_string_postgre
from .utils_log import log_decorator


@log_decorator
@validate_call
def read_csv_file(path: Path, delimiter: str) -> pd.DataFrame:
    """
    Read a CSV file into a pandas DataFrame.

    Args:
        path (Path): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If any other error occurs while reading the file.
    """
    try:
        if Path(path).is_file() == False:
            raise FileNotFoundError
        else:
            df = pd.read_csv(
                path, delimiter=delimiter, encoding="utf-8", header=0, index_col=False
            )
            return df
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"O arquivo para carregamento não foi encontrado. ERROR: {e}"
        )
    except Exception:
        raise Exception


def chuncker(seq, size):
    """Criação do chunker para controle da barra de progresso."""
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


@log_decorator
@validate_call
def load_table_postgre(df, table: str, schema: str) -> None:
    """
    Load a pandas DataFrame into a PostgreSQL table.

    Args:
        df (DataFrame): The DataFrame to be loaded into the table.
        table (str): The name of the table in the PostgreSQL database.
        schema (str): The name of the schema in the PostgreSQL database.

    Returns:
        None
    """
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
    print(f"Carga da tabela {table} finalizada com sucesso.")
