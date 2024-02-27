from pathlib import Path
from time import perf_counter

import pandas as pd
import pandera as pa
from modules.config import create_connection_string_postgre, test_connection_postgre
from modules.extract_data import extract_data_pd
from modules.load_data import load_table_postgre, read_csv_file
from modules.schemas import ImportWeatherStationSchema
from modules.transform_data import aggregate_df_using_duckdb, aggregate_df_using_polars


@pa.check_output(ImportWeatherStationSchema, lazy=True)
def load_csv_to_dataframe() -> pd.DataFrame:
    """Carrega os dados do CSV/TXT para um pandas dataframe."""
    try:
        path = Path(
            r"C:\Users\User\Desktop\bootcamp\bootcamp-eng-dados\src\projeto-01\data\measurements.txt"
        )
        df_weather_stations = read_csv_file(
            path=path,
            delimiter=";",
        )
        print("Arquivo Weather Stations validado com sucesso.")
    except Exception as e:
        print(f"Houve algum erro na leitura do arquivo Weather Stations.\nERROR: {e}")

    return df_weather_stations


def load_csv_weather_stations() -> None:
    """Realiza a leitura do dataframe e faz o load no banco de dados."""
    try:
        load_table_postgre(
            df=load_csv_to_dataframe(),
            table="raw_weather_stations",
            mode="replace",
            schema="public",
        )
        print("O arquivo foi carregado no banco de dados.")
    except Exception as e:
        print(
            f'Houve algum erro na execução do módulo "load_data_postgre.py"\nERROR: {e}'
        )


def main() -> None:
    try:
        # Testa a conexão com o banco de dados
        # test_connection_postgre()

        # Carrega as informações para o banco de dados
        # load_csv_weather_stations()

        # Executa a função de extração
        query = "SELECT * FROM public.raw_weather_stations"
        df_pd = extract_data_pd(create_connection_string_postgre(), query)

        # Excecuta a função de agg usando Polars
        name_cols = df_pd.columns.to_list()
        groupby_col = name_cols[0]
        measure_col = name_cols[1]

        time_start = perf_counter()
        df_polars = aggregate_df_using_polars(df_pd, groupby_col, measure_col)
        time_polars = perf_counter() - time_start
        print(df_polars)
        print(f"Polars took: {time_polars:.2f} seconds.")

        # Executa a função de agg usando DuckDB
        time_start = perf_counter()
        df_duckdb = aggregate_df_using_duckdb(df_pd, groupby_col, measure_col)
        time_duckdb = perf_counter() - time_start
        print(df_duckdb)
        print(f"DuckDB took: {time_duckdb:.2f} seconds.")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
