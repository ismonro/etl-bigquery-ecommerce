import pandas as pd
import os
from src.config import DATA_RAW_DIR

def load_raw_data():
    files = {
        'orders': 'raw_orders.parquet',
        'order_items': 'raw_order_items.parquet',
        'products': 'raw_products.parquet',
        'users': 'raw_users.parquet'
    }

    data = {}

    for key, filename in files.items():
        path = os.path.join(DATA_RAW_DIR, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f'❌ No se encontró el archivo: {filename} en {DATA_RAW_DIR}.')
        
        data[key] = pd.read_parquet(path)
    
    print('Datos RAW cargados correctamente')
    return data


def clean_orders(df):
    pass

def clean_order_items(df):
    pass

def clean_products(df):
    pass

def clean_users(df):
    pass

def build_sales_fact(orders, order_items, products, users):
    pass

def save_processed(df, filename):
    pass

def transform_all():
    pass

if __name__ == '__main__':
    load_raw_data()
