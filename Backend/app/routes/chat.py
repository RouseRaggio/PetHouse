from fastapi import APIRouter
from pydantic import BaseModel
from ollama import Client

router = APIRouter(tags=["Chat"])

client = Client(
    host="http://host.docker.internal:11434"
)

class ChatRequest(BaseModel):
    mensaje: str

@router.post("/chat")
def chat(data: ChatRequest):

    response = client.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": """
                Eres el asistente virtual de PetHouse.

                Ayudas a los usuarios con:
                - adopciones
                - mascotas
                - servicios veterinarios
                - productos

                Responde siempre en español.
                """
            },
            {
                "role": "user",
                "content": data.mensaje
            }
        ]
    )

    return {
        "respuesta": response.message.content
    }