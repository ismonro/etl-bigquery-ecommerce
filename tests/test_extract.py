from src.extract import run_query, save_raw

if __name__== '__main__':
    query = """
        SELECT order_id, user_id
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        LIMIT 5
    """

    df = run_query(query)
    print(df)

