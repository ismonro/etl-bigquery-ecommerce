import os
import pandas as pd
from src.extract import run_query, save_raw, extract_all, get_bigquery_client
from src.config import DATA_RAW_DIR, PROJECT_ID
from unittest.mock import MagicMock


def test_big_query_clien(monkeypatch):
    "Verifica que el cliente se cree usando la Service Account y credenciales correctamente"
    mock_from_json = MagicMock()

    # Parcheamos la función interna de Google BigQuery
    monkeypatch.setattr(
        "google.cloud.bigquery.Client.from_service_account_json",
        mock_from_json
    )

    client = get_bigquery_client()

    # Comprobamos que intentó instancearse con el método correcto
    mock_from_json.assert_called_once()



def test_run_query(monkeypatch):
    # Preparación de la respuesta ficticia y el objeto de juguete
    expected_df = pd.DataFrame({'order_id': [1], 'user_id': [10]})

    mock_client = MagicMock()
    mock_client.query.return_value.to_dataframe.return_value = expected_df

    # Interceptar el cliente BigQuery con monkeypatch
    monkeypatch.setattr('src.extract.get_bigquery_client', lambda: mock_client)

    # Ejecutar la función real que queremos probar
    df = run_query('SELECT * FROM tabla')

    # Comprobar que todo ocurrió según lo planificado
    mock_client.query.assert_called_once_with('SELECT * FROM tabla')
    pd.testing.assert_frame_equal(df, expected_df)

def test_save_raw(monkeypatch, tmp_path):
    """Verifica que se crea el directorio y guarde el archivo en parquet correctamente"""
    # tmp_path es una fixture de pytest que crea una carpeta temporal segura
    monkeypatch.setattr('src.extract.DATA_RAW_DIR', str(tmp_path))

    df_sample = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
    filename = 'test_data.parquet'

    save_raw(df_sample, filename)

    # Validar físicamente que el archivo existe en la carpeta temporal
    expected_file = tmp_path / filename
    assert expected_file.exists()

    # Validar que el contenido guardado en parquet sea idéntico al original
    saved_df = pd.read_parquet(expected_file)
    pd.testing.assert_frame_equal(saved_df, df_sample)




