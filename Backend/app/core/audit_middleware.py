from functools import wraps
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import Request
from app.controllers.audit_log_controller import log_action


def audit_action(
    action: str,
    resource: str,
    resource_id_param: Optional[str] = None,
    include_changes: bool = True
):
    """
    Decorator to automatically log actions.
    
    Args:
        action: "create", "update", "delete", "login", etc
        resource: "user", "pet", "adoption", etc
        resource_id_param: Name of parameter in kwargs that contains the resource_id
        include_changes: Whether to capture changes
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Try to extract db and current_user from args/kwargs
            db: Optional[Session] = None
            user_id: Optional[int] = None
            resource_id: Optional[int] = None
            ip_address: Optional[str] = None
            
            # Find db session (usually first or last argument)
            for arg in args:
                if isinstance(arg, Session):
                    db = arg
                    break
            
            # Check kwargs for db
            if not db and 'db' in kwargs:
                db = kwargs['db']
            
            # Find current_user
            if 'current_user' in kwargs and kwargs['current_user']:
                user_id = kwargs['current_user'].get('id')
            elif 'current_admin' in kwargs and kwargs['current_admin']:
                user_id = kwargs['current_admin'].get('id')
            
            # Find resource_id
            if resource_id_param and resource_id_param in kwargs:
                resource_id = kwargs[resource_id_param]
            
            # Get changes if available
            changes = None
            if include_changes and 'data' in kwargs:
                data = kwargs['data']
                if hasattr(data, 'dict'):
                    changes = data.dict()
                elif isinstance(data, dict):
                    changes = data
            
            # Log the action
            if db:
                try:
                    log_action(
                        db=db,
                        user_id=user_id,
                        action=action,
                        resource=resource,
                        resource_id=resource_id,
                        changes=changes,
                        ip_address=ip_address,
                        status="success"
                    )
                except Exception as e:
                    # Don't fail the request if logging fails
                    print(f"Audit logging error: {str(e)}")
            
            return result
        return wrapper
    return decorator


def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    if request.client:
        return request.client.host
    return "unknown"
