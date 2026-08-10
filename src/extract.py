import os
from google.cloud import bigquery
import pandas as pd
from src.config import PROJECT_ID, CREDENTIALS_PATH, DATA_RAW_DIR


def get_bigquery_client():
    """
    Crea y devuelve un cliente autentificado de Bigquery usando la service account
    """
    return bigquery.Client.from_service_account_json(
        CREDENTIALS_PATH,
        project:=PROJECT_ID
    )

def run_query(query:str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en Bigquery y devuelve un dataframe de pandas
    """
    client = get_bigquery_client()
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

def save_raw(df: pd.DataFrame, filename = str):
    """
    Guarda un dataframe en formato parquet dentro de data/raw/
    """
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    filepath = os.path.join(DATA_RAW_DIR, filename)
    
