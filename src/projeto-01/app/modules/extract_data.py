import pandas as pd
from pydantic import validate_call
from sqlalchemy import create_engine

from .utils_log import log_decorator, time_measure_decorator


@log_decorator
@time_measure_decorator
@validate_call
def extract_data_pd(connection_string: str, query: str) -> pd.DataFrame:
    """
    Extracts data from a database using a provided SQL query and returns it as a pandas DataFrame.

    Args:
        connection_string (str): The connection string to connect to the database.
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the query.
    """
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
        df = pd.read_sql_query(query, conn)
    return df
