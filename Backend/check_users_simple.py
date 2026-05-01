#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.user_model import User

def check_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role_id}, Active: {user.is_active}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()