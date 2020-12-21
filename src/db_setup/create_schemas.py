import os
import psycopg2

if __name__ == "__main__":
    pg_conn = psycopg2.connect(
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT']
    )

    cur = pg_conn.cursor()
    cur.execute('CREATE SCHEMA IF NOT EXISTS dimensions;');
    cur.execute('CREATE SCHEMA IF NOT EXISTS fact_tables;');

    pg_conn.commit()
    pg_conn.close()

    print("Connection to PostgreSQL in create_schemas.py has been closed.")
