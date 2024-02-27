import duckdb
import pandas as pd
import pandera as pa
import polars as pl
from pydantic import validate_call

from .schemas import ImportWeatherStationSchema, TransformWeatherStationSchema


@validate_call
@pa.check_input(ImportWeatherStationSchema, lazy=True)
def aggregate_df_using_polars(df, groupby_col: str, measure_col: str) -> pl.DataFrame:
    """Função que agrega um dataframe usando Polars."""
    try:
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

    except Exception as e:
        print(f"Erro ao transformar o dataframe com Polars.\nERROR: {e}")


@validate_call
@pa.check_input(ImportWeatherStationSchema, lazy=True)
@pa.check_output(TransformWeatherStationSchema, lazy=True)
def aggregate_df_using_duckdb(df, groupby_col: str, measure_col: str):
    """ "Função que agraga um dataframe usando DuckDB."""
    try:
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

    except Exception as e:
        print(f"Erro ao transformar o dataframe com DuckDB.\nERROR: {e}")
