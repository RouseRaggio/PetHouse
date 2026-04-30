from app.db.session import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE pets ADD COLUMN gps_status VARCHAR DEFAULT 'none'"))
            print("Columna gps_status añadida a pets")
        except Exception as e:
            print(f"Aviso: gps_status ya existe o error: {e}")
            
        try:
            conn.execute(text("ALTER TABLE pets ADD COLUMN gps_imei VARCHAR"))
            print("Columna gps_imei añadida a pets")
        except Exception as e:
            print(f"Aviso: gps_imei ya existe o error: {e}")
        
        conn.commit()

if __name__ == "__main__":
    migrate()
