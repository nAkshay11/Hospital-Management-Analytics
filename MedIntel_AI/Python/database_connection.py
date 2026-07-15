import psycopg2
from config import *

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ PostgreSQL Connected Successfully")
        return connection

    except Exception as e:
        print("❌ Connection Failed")
        print(e)