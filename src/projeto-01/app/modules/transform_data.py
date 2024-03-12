import duckdb
import pandas as pd
import pandera as pa
import polars as pl
from pydantic import validate_call

from .schemas import ImportWeatherStationSchema, TransformWeatherStationSchema
from .utils_log import log_decorator, time_measure_decorator


@log_decorator
@time_measure_decorator
@validate_call
@pa.check_input(ImportWeatherStationSchema, lazy=True)
def aggregate_df_using_polars(df, groupby_col: str, measure_col: str) -> pl.DataFrame:
    """
    Aggregate a DataFrame using Polars.

    If the input DataFrame is a pandas DataFrame, it will be converted to a Polars DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        groupby_col (str): The column to group by.
        measure_col (str): The column to aggregate.

    Returns:
        pl.DataFrame: The aggregated DataFrame, containing maximum, minimum, and mean values of the measure_col for each group in groupby_col, sorted by groupby_col.
    """
    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)

    df_grouped = (
        df.groupby(by=groupby_col)
        .agg(
            max=pl.col(measure_col).max().alias(f"max_{measure_col}"),
            min=pl.col(measure_col).min().alias(f"min_{measure_col}"),
            mean=pl.col(measure_col).mean().alias(f"mean_{measure_col}"),
        )
        .sort(groupby_col)
    )
    return df_grouped


@log_decorator
@time_measure_decorator
@validate_call
@pa.check_input(ImportWeatherStationSchema, lazy=True)
@pa.check_output(TransformWeatherStationSchema, lazy=True)
def aggregate_df_using_duckdb(df, groupby_col: str, measure_col: str) -> pd.DataFrame:
    """
    Aggregate a DataFrame using DuckDB.

    Args:
        df (DataFrame): The input DataFrame.
        groupby_col (str): The column to group by.
        measure_col (str): The column to aggregate.

    Returns:
        pd.DataFrame: The aggregated DataFrame, containing maximum, minimum, and mean values of the measure_col for each group in groupby_col, sorted by groupby_col.
    """
    if isinstance(df, pl.DataFrame):
        df = pl.to_pandas(df)
    df_grouped = duckdb.query(
        f"""SELECT {groupby_col} as {groupby_col},
                        MAX({measure_col}) as max_{measure_col},
                        MIN({measure_col}) as min_{measure_col},
                        AVG({measure_col}) as avg_{measure_col}
                FROM df
                GROUP BY {groupby_col}
                ORDER BY {groupby_col}
             """
    ).to_df()
    return df_grouped
