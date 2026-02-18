from fastapi import APIRouter, HTTPException
from app.controllers.role_controller import RoleController
from app.models.role_model import Role

router = APIRouter(
    tags=["Roles"]
)

nuevo_rol = RoleController()


@router.post("/create_role")
async def create_role(role: Role):
    return nuevo_rol.create_role(role)


@router.get("/get_role/{role_id}", response_model=Role)
async def get_role(role_id: int):
    return nuevo_rol.get_role(role_id)


@router.get("/get_roles/")
async def get_roles():
    return nuevo_rol.get_roles()


@router.put("/update_role/{role_id}")
async def update_role(role_id: int, role: Role):
    return nuevo_rol.update_role(role_id, role)


@router.delete("/delete_role/{role_id}")
async def delete_role(role_id: int):
    nuevo_rol.delete_role(role_id)
    return {"message": "Rol eliminado correctamente"}
