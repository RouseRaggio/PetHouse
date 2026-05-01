from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from app.models.audit_log_model import AuditLog
from app.schemas.audit_log_schema import AuditLogCreate, AuditLogResponse, AuditLogFilter


def log_action(
    db: Session,
    user_id: Optional[int],
    action: str,
    resource: str,
    resource_id: Optional[int] = None,
    changes: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    status: str = "success",
    details: Optional[str] = None
) -> AuditLog:
    """Log an action to the audit trail"""
    audit = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        ip_address=ip_address,
        status=status,
        details=details,
        timestamp=datetime.now(timezone.utc)
    )
    if changes:
        audit.set_changes(changes)
    
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def get_audit_logs(
    db: Session,
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    resource: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
) -> List[AuditLog]:
    """Get filtered audit logs"""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if action:
        query = query.filter(AuditLog.action == action)
    if resource:
        query = query.filter(AuditLog.resource == resource)
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    # Order by most recent first
    query = query.order_by(AuditLog.timestamp.desc())
    
    total = query.count()
    logs = query.limit(limit).offset(offset).all()
    
    return logs


def get_audit_log_by_id(db: Session, log_id: int) -> AuditLog:
    """Get a specific audit log"""
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail=f"Audit log {log_id} not found")
    return log


def get_user_audit_logs(db: Session, user_id: int, limit: int = 50) -> List[AuditLog]:
    """Get all audit logs for a specific user"""
    return (
        db.query(AuditLog)
        .filter(AuditLog.user_id == user_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(limit)
        .all()
    )
