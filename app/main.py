from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.pet_routes import router as pet_router
from app.routes.adoption_routes import router as adoption_router
from app.routes.role_routes import router as role_router
from app.db.base import Base
from app.models.user_model import User
from app.models.role_model import Role
from app.models.permission_model import Permission
from app.models.role_permission_model import RolePermission
from app.models.pet_model import Pet
from app.models.adoption_status_model import AdoptionStatus
from app.models.adoption_model import Adoption
from app.models import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.db.session import engine
from app.routes.adoption_status_routes import router as adoption_status_router
from app.routes.role_permission_routes import router as role_permission_router
from app.routes.permission_routes import router as permission_router
from app.routes.tracker_routes import router as tracker_router
from app.routes.tracker_location_routes import router as tracker_location_router


app = FastAPI()

Base.metadata.create_all(bind=engine)
# Crear carpeta uploads si no existe
if not os.path.exists("uploads"):
    os.makedirs("uploads")

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(user_router)
app.include_router(pet_router)
app.include_router(adoption_router)
app.include_router(role_router)
app.include_router(adoption_status_router)
app.include_router(role_permission_router)
app.include_router(permission_router)
app.include_router(tracker_router)
app.include_router(tracker_location_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
