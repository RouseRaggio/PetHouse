from app.db.session import engine
from sqlalchemy import text

def check():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT id, name, species, status, deleted_at FROM pets")).fetchall()
        for row in res:
            print(row)

if __name__ == "__main__":
    check()
