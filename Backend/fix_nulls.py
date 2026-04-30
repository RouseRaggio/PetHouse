from app.db.session import engine
from sqlalchemy import text

def fix():
    with engine.connect() as conn:
        conn.execute(text("UPDATE pets SET gps_status = 'none' WHERE gps_status IS NULL"))
        conn.commit()
        print("Valores NULL en gps_status corregidos.")

if __name__ == "__main__":
    fix()
