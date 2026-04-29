#!/usr/bin/env python3
"""
Script to update existing user roles.
Changes users with role_id 1 (except superadmin) to role_id 2 (normal users).
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User, Role
from app.core.security import hash_password

def update_user_roles():
    """Update existing user roles"""
    db: Session = next(get_db())

    try:
        admin_role = db.query(Role).filter_by(name="Admin").first()
        user_role = db.query(Role).filter_by(name="Usuario").first()

        if not admin_role or not user_role:
            print("No se encontró el rol Admin o Usuario. Ejecuta el seeder primero.")
            return

        # Convertir cualquier superadmin antiguo a usuario normal
        superadmins = db.query(User).filter(User.role_id == 3).all()
        for user in superadmins:
            print(f"Convirtiendo superadmin {user.email} a usuario normal")
            user.role_id = user_role.id

        # Actualizar admin@gmail.com a admin con password secret
        admin_user = db.query(User).filter(User.email == "admin@gmail.com").first()

        if admin_user:
            admin_user.role_id = admin_role.id
            admin_user.password = hash_password("secret")
            print(f"Actualizando credenciales de admin: {admin_user.email}")
        else:
            # Si no existe admin@gmail.com, usar admin@admin.com como base
            legacy_admin = db.query(User).filter(User.email == "admin@admin.com").first()
            if legacy_admin:
                legacy_admin.email = "admin@gmail.com"
                legacy_admin.role_id = admin_role.id
                legacy_admin.password = hash_password("secret")
                print(f"Actualizando credenciales de admin: {legacy_admin.email}")
            else:
                print("No se encontró un usuario admin existente para actualizar.")

        # Convertir todos los usuarios con role_id 1 que no son admin@gmail.com a usuario normal
        users_to_update = db.query(User).filter(
            User.role_id == 1,
            User.email != 'admin@gmail.com'
        ).all()

        print(f"Found {len(users_to_update)} users with role_id 1 to update to role_id 2:")
        for user in users_to_update:
            print(f"  - {user.email} (ID: {user.id})")
            user.role_id = user_role.id

        db.commit()

        print(f"\nSuccessfully updated {len(users_to_update)} users to role_id 2 (Usuario normal).")

        roles = db.query(Role).all()
        for role in roles:
            count = db.query(User).filter(User.role_id == role.id).count()
            print(f"Role {role.id} ({role.name}): {count} users")

    except Exception as e:
        print(f"Error updating user roles: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_user_roles()