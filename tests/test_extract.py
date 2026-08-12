import os
import pandas as pd
from src.extract import run_query, save_raw, extract_all
from src.config import DATA_RAW_DIR, PROJECT_ID

def test_run_query():
    """
    Prueba básica para ejecutar una consulta pequeña y verificar que devuelve un dataframe
    """
    query = """
        SELECT order_id, user_id
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        LIMIT 5
    """

    df = run_query(query)

    print('Resultado de run_query():')
    print(df.head())

    assert isinstance(df, pd.DataFrame), "run_query no devolvió un dataframe"
    assert len(df) > 0, "La consulta devolvió un Dataframe vacío"

def test_save_query():
    """
    Prueba básica para ejecutar una consulta pequeña y verificar que devuelve un dataframe
    """
    df = pd.DataFrame({'col': [1, 2], 'col2': ['a', 'b']})
    filename = 'test_save_raw.parquet'

    save_raw(df, filename)

    filepath = os.path.join(DATA_RAW_DIR, filename)
    assert os.path.exists(filepath), "El archivo no se guardó correctamente"

    print(f'Archivo {filename} guardado correctamente')

def test_extract_all():
    """
    Prueba completa: Ejecutar extract all y verificar que genera los archivos esperados
    """
    extract_all()

    expected_files = [
        "raw_orders.parquet",
        "raw_order_items.parquet",
        "raw_products.parquet",
        "raw_users.parquet",
    ]

    for file in expected_files:
        filepath = os.path.join(DATA_RAW_DIR, file)
        assert os.path.exists(filepath), f'Falta el archivo {file}'
        print(f'{file} generado correctamente')

def test_get_bigquery_client():
    """
    Verifica que la función devuelve un cliente válido de Bigquery
    """
    client = test_get_bigquery_client()

    # Comprobación 1: El objeto existe
    assert client is not None, "get_bigquery_client devolvió None"

    # Comprobación 2: es del tipo correcto
    from google.cloud.bigquery import Client
    assert isinstance(client, Client), "get_bigquery_client no devolvió un objeto Client"

    # Comprobación 3: El cliente está configurado con el proyecto correcto
    assert client.project == PROJECT_ID, "El cliente no está usando el PROJECT_ID correcto"

    print("✔ Cliente BigQuery creado correctamente:", client.project)


if __name__ == '__main__':
    test_run_query()
    test_save_query()
    test_extract_all()
    test_get_bigquery_client()
