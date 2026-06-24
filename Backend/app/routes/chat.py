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
                Eres 'Petro', el asistente virtual de PetHouse.

                Ayudas a los usuarios con:
                - adopciones
                - mascotas
                - servicios veterinarios
                - productos
                
                Reglas:
                - Responde siempre en español y en inglés si y solo si el usuario lo solicita.
                - Respuestas concisas sin adiciones (máximo 4 oraciones)
                - Solo responde preguntas sobre mascotas y PetHouse. Si preguntan otra cosa, redirige al tema.
                - Usa emojis de animales ocasionalmente
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