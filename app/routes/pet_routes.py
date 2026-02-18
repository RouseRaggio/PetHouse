from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import os

from app.controllers.pet_controller import PetController

router = APIRouter(
    tags=["Mascotas"]
)
pet_controller = PetController() 

UPLOAD_FOLDER = "uploads"

@router.post("/create_pet")
async def create_pet(
    nombre: str = Form(...),
    especie: str = Form(...),
    edad: int = Form(...),
    descripcion: str = Form(...),
    user_id: int = Form(...),
    imagen: UploadFile = File(...)
):
    
    if imagen.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG o PNG"
        )

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, imagen.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    pet_data = {
        "nombre": nombre,
        "especie": especie,
        "edad": edad,
        "descripcion": descripcion,
        "imagen": imagen.filename,
        "user_id": user_id
    }

    return pet_controller.create_pet(pet_data)


@router.get("/get_pets")
async def get_pets():
    return pet_controller.get_pets()


@router.put("/update_pet/{pet_id}/{user_id}")
async def update_pet(
    pet_id: int,
    user_id: int,
    nombre: str = Form(...),
    especie: str = Form(...),
    edad: int = Form(...),
    descripcion: str = Form(...)
):
    pet_data = {
        "nombre": nombre,
        "especie": especie,
        "edad": edad,
        "descripcion": descripcion
    }

    result = pet_controller.update_pet(pet_id, pet_data, user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    return result


@router.delete("/delete_pet/{pet_id}/{user_id}")
async def delete_pet(pet_id: int, user_id: int):
    result = pet_controller.delete_pet(pet_id, user_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")

    return result
