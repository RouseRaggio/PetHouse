#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.models.audit_log_model import AuditLog
from datetime import datetime, timezone

def create_sample_audit_logs():
    db = SessionLocal()
    try:
        # Crear algunos logs de ejemplo
        logs = [
            AuditLog(
                user_id=1,
                action="login",
                resource="user",
                resource_id=1,
                details="Login exitoso",
                status="success",
                timestamp=datetime.now(timezone.utc)
            ),
            AuditLog(
                user_id=1,
                action="create",
                resource="pet",
                resource_id=1,
                details="Mascota creada",
                status="success",
                timestamp=datetime.now(timezone.utc)
            ),
            AuditLog(
                user_id=1,
                action="update",
                resource="user",
                resource_id=2,
                details="Usuario actualizado",
                status="success",
                timestamp=datetime.now(timezone.utc)
            )
        ]

        for log in logs:
            db.add(log)

        db.commit()
        print("Sample audit logs created successfully")

    except Exception as e:
        print(f"Error creating sample logs: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_audit_logs()