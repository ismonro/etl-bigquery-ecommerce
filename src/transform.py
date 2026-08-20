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
    # Converir a fechas
    date_cols = ['created_at', 'shipped_at', 'delivered_at']

    for date in date_cols:
        df[date] = pd.to_datetime(df[date], errors= 'coerce')
    
    # Eliminación de duplicados
    df = df.drop_duplicates(subset = 'order_id', ignore_index = True)
    # Filtrado de estados
    valid_values = ['Complete', 'Processing', 'Shipped']

    df = df[df['status'].isin(valid_values)]

    # Cálculo de métricas logísticas
    df['shipping_time_days'] = (df['shipped_at'] - df['created_at']).dt.days
    df['delivery_time_days'] = (df['delivered_at'] - df['shipped_at']).dt.days
    df['total_fulfillment_days'] = (df['delivered_at'] - df['created_at']).dt.days
    # Casting de tipos
    cast_map = {
        'order_id': int,
        'user_id': int,
        'status': str,
        'num_of_item': int
    }

    for col, dtype in cast_map.items():
        df[col] = df[col].astype(dtype, errors = 'raise')

    return df

def clean_order_items(df):
    # Convertir fechas si las hay
    date_cols = ['created_at']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors= 'coerce')

    # Eliminar duplicados
    df = df.drop_duplicates(subset = 'id', ignore_index = True)

    # Eliminar órdenes con id_nulo
    df = df.dropna(subset = 'order_id')

    # Asegurar tipos correctos
    cast_map = {
        'id': int,
        'order_id': int,
        'user_id': int,
        'product_id': int,
        'sale_price': float,
        'status': str
    }

    for col, dtype in cast_map.items():
        df[col] = df[col].astype(dtype)

    # FIltrar estados válidos
    valid_status = ['Complete', 'Processing', 'Shipped']

    df = df[df['status'].isin(valid_status)]

    return df


def clean_products(df):
    # Borrar duplicados
    df = df.drop_duplicates(subset = ['id'], ignore_index = True)

    # Asegurar tipos correctos
    cast_map = {
        'id': int,
        'category': str,
        'name': str,
        'brand': str,
        'cost': float,
        'retail_price': float,
        'department': str
    }

    for col, dtype in cast_map.items():
        df[col] = df[col].astype(dtype)

    # Filtro de valores erróneos en retail_price o costo menor que 0
    df = df[(df['cost'] > 0) & (df['retail_price'] > 0)]

    # Métricas de ayuda
    df['margin'] = df['retail_price'] - df['cost']

    return df

def clean_users(df):

   # Convertir a fecha
    col_dates = ['created_at']

    for col in col_dates:
        df[col] = pd.to_datetime(df[col], errors= 'coerce')

    # Eliminar duplicados
    df = df.drop_duplicates(subset = ['id'], ignore_index = True)

    # Asegurar tipos correctos
    cast_map = {
        'id': int,
        'age': int,
        'gender': str,
        'country': str,
        'city': str,
        'traffic_source': str
    }

    for col, dtype in cast_map.items():
        df[col] = df[col].astype(dtype)

 
    # Eliminar usuarios sin id
    df = df.dropna(subset = ['id'])

    return df

def build_sales_fact(orders, order_items, products, users):

    if 'user_id' in order_items.columns:
        order_items = order_items.drop(columns = ['user_id'])

    products = products.rename(columns = {'id': 'product_id'})
    users = users.rename(columns = {'id': 'user_id'})

    fact_sales = pd.merge(
        orders,
        order_items,
        how= 'inner',
        on= 'order_id'
    )

    fact_sales = pd.merge(
        fact_sales,
        products,
        how= 'inner',
        on= 'product_id'
    )

    fact_sales = pd.merge(
        fact_sales,
        users,
        how= 'inner',
        on= 'user_id'
    )

    return fact_sales
    

def save_processed(df, filename):
    pass

def transform_all():
    pass

if __name__ == '__main__':
    data = load_raw_data()
    orders = data['orders']
    order_items = data['order_items']
    products = data['products']
    users = data['users']

    fact_sales = build_sales_fact(orders, order_items, products, users)
    print(fact_sales.info())




