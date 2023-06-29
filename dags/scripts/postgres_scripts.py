from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2

dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', 'postgres.env')
load_dotenv(dotenv_path)

host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
database = os.getenv('POSTGRES_DB')

# Connect to PostgreSQL
def connect_postgres():
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    return conn

# Create table
def create_table(schema_name):
    conn = connect_postgres()
    cur = conn.cursor()

    # Schema for table
    with open(f"{schema_name}.sql", "r") as f:
        create_table_sql = f.read()

    try:
        cur.execute(create_table_sql)
        conn.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")

    cur.close()
    conn.close()

# Insert data into table
def load_data(df: pd.DataFrame, table_name):
    conn = connect_postgres()
    cur = conn.cursor()

    # Insert data into table
    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")

    cur.close()
    conn.close()
