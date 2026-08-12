from src.extract import run_query, save_raw

if __name__== '__main__':
    query = {
        "users.parquet": """
            SELECT
                id,
                age,
                gender,
                country,
                city,
                traffic_source,
                created_at
            FROM `bigquery-public-data.thelook_ecommerce.users`
            LIMIT 5
        """
    }

    for filename, sql in query.items():
        df = run_query(sql)
        save_raw(df, filename)

