import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="ep-damp-block-ai81i5p8-pooler.c-4.us-east-1.aws.neon.tech",
            port="5432",
            user="neondb_owner",
            password="npg_ReiUD27Fftnw",
            dbname="neondb",
            sslmode="require"
        )
        return conn
    except Exception as e:
        print("Error conectando a la base de datos:", e)
        return None
