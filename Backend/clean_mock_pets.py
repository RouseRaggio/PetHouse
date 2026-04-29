#!/usr/bin/env python3
"""
Script to clean up mock pet data from the database.
Removes pets with example.com URLs that are not real.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Pet, Adoption

def clean_mock_pets():
    """Remove pets with mock/example URLs"""
    db: Session = next(get_db())

    try:
        # Find pets with example.com URLs
        mock_pets = db.query(Pet).filter(
            Pet.image_url.like('https://example.com/%')
        ).all()

        print(f"Found {len(mock_pets)} mock pets to remove:")

        for pet in mock_pets:
            print(f"  - {pet.name} (ID: {pet.id}) - {pet.image_url}")

        # First, delete related adoptions
        adoption_delete_count = db.query(Adoption).filter(
            Adoption.pet_id.in_([pet.id for pet in mock_pets])
        ).delete()

        print(f"\nDeleted {adoption_delete_count} related adoptions.")

        # Then delete the mock pets
        deleted_count = db.query(Pet).filter(
            Pet.image_url.like('https://example.com/%')
        ).delete()

        db.commit()

        print(f"Successfully removed {deleted_count} mock pets from database.")

        # Show remaining pets
        remaining_pets = db.query(Pet).all()
        print(f"\nRemaining pets in database: {len(remaining_pets)}")
        for pet in remaining_pets:
            print(f"  - {pet.name} (ID: {pet.id}) - Status: {pet.status}")

    except Exception as e:
        print(f"Error cleaning mock pets: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_mock_pets()