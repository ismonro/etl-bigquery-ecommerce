import pandas as pd
import pytest
from src.transform import load_raw_data
from src.config import DATA_RAW_DIR

def test_load_raw_data_ok(monkeypatch, tmp_path):
    # 1. Redirigir LOAD_RAW_DATA a la carpeta temporal
    monkeypatch.setattr('src.transform.DATA_RAW_DIR', str(tmp_path))

    # 2. Diccionario de dataframes de ejemplo
    df_examples = {
        'df_orders': {'id': [1], 'user_id': [10]},
        'df_items': {'id': [1], 'order_id': [1], 'product_id': [20]},
        'df_products': {'id': [100], 'name': ['A'], 'cost': [10], 'retail_price': [20]},
        'df_users': {'id': [10], 'country': ['ES']}
    }

    # 3.Convertir a Dataframes

    dfs = {name : pd.DataFrame(data) for name, data in df_examples.items()}

    # 4. Mapeo a nombres de archivo RAW
    file_map = {
        'df_orders': 'raw_orders.parquet',
        'df_items': 'raw_order_items.parquet',
        'df_products': 'raw_products.parquet',
        'df_users': 'raw_users.parquet'
    }

    # 5. Guardar todos los dataframes en tmp_path
    for df_name, df in dfs.items():
        filename = file_map[df_name]
        df.to_parquet(tmp_path / filename)

    # 6. Ejecutar la función real
    data = load_raw_data()

    # 7. Validar que los Dataframe cargados son idénticos
    assert_map = {
        'orders': 'df_orders',
        'order_items': 'df_items',
        'products': 'df_products',
        'users': 'df_users'
    }

    for key_load, key_df in assert_map.items():
        pd.testing.assert_frame_equal(data[key_load], dfs[key_df])


