import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            dbname=os.getenv("DATABASE_NAME"),
            sslmode="require"
        )
        return conn
    except Exception as e:
        print("Error conectando a la base de datos:", e)
        return None
