import sys
sys.path.append('.')

from app.db.session import SessionLocal
from app.models.user_model import User

db = SessionLocal()
users = db.query(User).all()
print(f'Total users: {len(users)}')
for user in users:
    print(f"ID: {user.id}, Email: {user.email}, Role: {user.role_id}, Active: {user.is_active}")

db.close()