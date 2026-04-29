#!/usr/bin/env python3
"""
Script to run database seeders.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.seeders.superadmin_seeder import seed_admin

def run_seeders():
    """Run all database seeders"""
    db: Session = next(get_db())

    try:
        print("Running admin seeder...")
        seed_admin(db)
        print("Admin seeder completed successfully.")

    except Exception as e:
        print(f"Error running seeders: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()