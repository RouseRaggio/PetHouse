from fastapi import APIRouter, HTTPException
from app.controllers.user_controller import UserController
from app.models.user_model import User

router = APIRouter(
    tags=["Usuarios"]
)

nuevo_usuario = UserController()

@router.post("/create_user")
async def create_user(user: User):
    return nuevo_usuario.create_user(user)

@router.get("/get_user/{user_id}", response_model=User)
async def get_user(user_id: int):
    return nuevo_usuario.get_user(user_id)

@router.get("/get_users/")
async def get_users():
    return nuevo_usuario.get_users()

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: User):
    return nuevo_usuario.update_user(user_id, user)

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    nuevo_usuario.delete_user(user_id)
    return {"message": "Usuario eliminado correctamente"}
 