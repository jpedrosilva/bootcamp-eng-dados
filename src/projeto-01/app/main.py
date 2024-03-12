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
    """Carrega os dados do CSV/TXT para um pandas dataframe e faz a validação do output."""
    try:
        path = Path("./data/measurements.txt")
        df_weather_stations = read_csv_file(
            path=path,
            delimiter=";",
        )
        print("Arquivo Weather Stations validado com sucesso.")
    except Exception as e:
        print(f"Houve algum erro na leitura do arquivo Weather Stations.\nERROR: {e}")

    return df_weather_stations


def main() -> None:
    try:
        # Testa a conexão com o banco de dados
        test_connection_postgre()

        # Carrega as informações para o banco de dados
        load_table_postgre(
            df=load_csv_to_dataframe(), table="raw_weather_stations", schema="public"
        )

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

        # Executa a função de agg usando DuckDB
        time_start = perf_counter()
        df_duckdb = aggregate_df_using_duckdb(df_pd, groupby_col, measure_col)
        time_duckdb = perf_counter() - time_start

        # Criando tabela de benchmark no banco de dados
        data_benchmark = {
            "framework": ["Polars", "DuckDB"],
            "time_elapsed": [round(time_polars, 2), round(time_duckdb, 2)],
        }
        df_benchmark = pd.DataFrame(data_benchmark)
        df_benchmark["dataset"] = "1MM rows"

        load_table_postgre(
            df=df_benchmark, table="benchmark_frameworks", schema="public"
        )

        # Leitura da tabela de benchmark
        query_bench = "SELECT * FROM public.benchmark_frameworks"
        df_bench = extract_data_pd(create_connection_string_postgre(), query_bench)
        print(df_bench)

        # Subindo a tabela com o dataframe tratado para o banco de dados
        load_table_postgre(df=df_duckdb, table="tb_aggregated_data", schema="public")

        # Leitura da tabela agregada
        query_agg = "SELECT * FROM tb_aggregated_data"
        df_agg = extract_data_pd(create_connection_string_postgre(), query_agg)
        print(df_agg)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
