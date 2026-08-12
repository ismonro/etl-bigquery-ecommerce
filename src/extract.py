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
        project=PROJECT_ID
    )

def run_query(query:str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL en Bigquery y devuelve un dataframe de pandas
    """
    client = get_bigquery_client()
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

def save_raw(df: pd.DataFrame, filename:str):
    """
    Guarda un dataframe en formato parquet dentro de data/raw/
    """
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    filepath = os.path.join(DATA_RAW_DIR, filename)
    df.to_parquet(filepath, index= False)
    print(f'Datos guardados en {filepath}')

def extract_all():
    queries = {
        "raw_orders.parquet": """
            SELECT
                order_id,
                user_id,
                status,
                created_at,
                shipped_at,
                delivered_at,
                num_of_item
            FROM `bigquery-public-data.thelook_ecommerce.orders`
            WHERE created_at >= '2023-01-01'
        """,
        "raw_order_items.parquet": """
            SELECT
                id,
                order_id,
                user_id,
                product_id,
                sale_price,
                status,
                created_at
            FROM `bigquery-public-data.thelook_ecommerce.order_items`
            WHERE created_at > '2023-01-01'
        """,
        "raw_products.parquet": """
            SELECT
                id,
                category,
                name,
                brand,
                cost,
                retail_price,
                department
            FROM `bigquery-public-data.thelook_ecommerce.products`
        """,
        "raw_users.parquet": """
            SELECT
                id,
                age,
                gender,
                country,
                city,
                traffic_source,
                created_at
            FROM `bigquery-public-data.thelook_ecommerce.users`
        """
    }

    for filename, query in queries.items():
        print(f"⏳ Ejecutando consulta para {filename}...")
        df = run_query(query)
        save_raw(df, filename)

    print(f'Extracción de {filename} completada correctamente')
        

    
