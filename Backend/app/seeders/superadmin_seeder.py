from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.core.security import hash_password


def seed_superadmin(db: Session):

    # Crear permisos base
    permissions_list = [
        "create_user",
        "read_user",
        "update_user",
        "delete_user"
    ]

    for perm_name in permissions_list:
        perm = db.query(Permission).filter_by(name=perm_name).first()
        if not perm:
            db.add(Permission(name=perm_name))

    db.commit()

    # Crear rol SUPERADMIN
    role = db.query(Role).filter_by(name="SUPERADMIN").first()

    if not role:
        role = Role(name="SUPERADMIN")
        db.add(role)
        db.commit()
        db.refresh(role)

    # Asignar todos los permisos al superadmin
    all_permissions = db.query(Permission).all()
    role.permissions = all_permissions
    db.commit()

    # Crear usuario superadmin
    user = db.query(User).filter_by(email="admin@admin.com").first()

    if not user:
        superadmin = User(
            nombre="Super Admin",
            email="admin@admin.com",
            password=hash_password("Admin123*"),
            role_id=role.id
        )
        db.add(superadmin)
        db.commit()
