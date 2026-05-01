from app.db.session import SessionLocal
from app.models.audit_log_model import AuditLog

db = SessionLocal()
count = db.query(AuditLog).count()
print(f'Audit logs count: {count}')

if count > 0:
    logs = db.query(AuditLog).limit(5).all()
    for log in logs:
        print(f"ID: {log.id}, Action: {log.action}, User: {log.user_id}, Resource: {log.resource}")

db.close()