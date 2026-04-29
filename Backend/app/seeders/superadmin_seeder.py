from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user_model import User
from app.models.role_model import Role
from app.models.permission_model import Permission
from app.core.security import hash_password


def seed_admin(db: Session):

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

    # Crear rol Admin y Usuario
    admin_role = db.query(Role).filter_by(name="Admin").first()
    if not admin_role:
        admin_role = Role(name="Admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    user_role = db.query(Role).filter_by(name="Usuario").first()
    if not user_role:
        user_role = Role(name="Usuario")
        db.add(user_role)
        db.commit()
        db.refresh(user_role)

    # Asignar todos los permisos al rol Admin
    all_permissions = db.query(Permission).all()
    admin_role.permissions = all_permissions
    db.commit()

    # Crear o actualizar usuario admin
    user = db.query(User).filter(or_(User.email == "admin@gmail.com", User.email == "admin@admin.com")).first()

    if not user:
        admin_user = User(
            name="Admin",
            last_name="",
            email="admin@gmail.com",
            password=hash_password("secret"),
            role_id=admin_role.id
        )
        db.add(admin_user)
    else:
        user.email = "admin@gmail.com"
        user.role_id = admin_role.id
        user.password = hash_password("secret")

    db.commit()
