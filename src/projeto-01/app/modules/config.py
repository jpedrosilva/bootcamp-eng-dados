from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


def load_db_settings() -> dict:
    """Carrega as credenciais de conexão do banco de dados."""
    dotenv_path = Path.cwd() / ".env"
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": getenv("POSTGRES_HOST"),
        "db_user": getenv("POSTGRES_USER"),
        "db_pass": getenv("POSTGRES_PASSWORD"),
        "db_name": getenv("POSTGRES_DB"),
        "db_port": getenv("POSTGRES_PORT"),
    }

    return settings


def create_connection_string_postgre() -> str:
    "Cria a string de conexão para o banco PostgreSQL."
    settings = load_db_settings()
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    return connection_string


def test_connection_postgre() -> None:
    try:
        engine = create_engine(create_connection_string_postgre())
        with engine.connect() as conn, conn.begin():
            print("A conexão com o banco de dados foi bem-sucedida.")
    except Exception as e:
        print(f"A conexão com o banco de dados não foi bem-sucedida.\nERROR: {e}")
