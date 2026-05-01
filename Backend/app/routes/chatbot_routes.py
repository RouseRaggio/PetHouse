from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

# Importaciones condicionales para evitar errores si no existen
try:
    from app.database import get_db
    from app.services.auth_service import get_current_user
    from app.models.user import User
    from app.services.chatbot_service import chatbot_service
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some dependencies not available for chatbot: {e}")
    DEPENDENCIES_AVAILABLE = False
    get_db = None
    get_current_user = None
    User = None
    chatbot_service = None

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str
    clear_context: Optional[bool] = False

class ChatResponse(BaseModel):
    response: str
    context_length: int

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    request: ChatRequest,
    current_user = Depends(get_current_user) if DEPENDENCIES_AVAILABLE else None,
    db = Depends(get_db) if DEPENDENCIES_AVAILABLE else None
):
    """
    Enviar un mensaje al chatbot y obtener respuesta.
    Requiere autenticación.
    """
    if not DEPENDENCIES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Servicio de chatbot no disponible")

    try:
        # Limpiar contexto si se solicita
        if request.clear_context:
            chatbot_service.clear_context()

        # Verificar si el modelo está disponible
        if not await chatbot_service.is_model_available():
            raise HTTPException(
                status_code=503,
                detail="El servicio de chatbot no está disponible. Verifica que Ollama esté ejecutándose."
            )

        # Generar respuesta
        response = await chatbot_service.generate_response(request.message)

        return ChatResponse(
            response=response,
            context_length=chatbot_service.get_context_length()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chatbot: {str(e)}")

@router.post("/clear")
async def clear_chat_context(
    current_user = Depends(get_current_user) if DEPENDENCIES_AVAILABLE else None,
    db = Depends(get_db) if DEPENDENCIES_AVAILABLE else None
):
    """
    Limpiar el contexto del chat.
    Requiere autenticación.
    """
    if not DEPENDENCIES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Servicio de chatbot no disponible")

    try:
        chatbot_service.clear_context()
        return {"message": "Contexto del chat limpiado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error limpiando contexto: {str(e)}")

@router.get("/status")
async def get_chatbot_status(
    current_user = Depends(get_current_user) if DEPENDENCIES_AVAILABLE else None,
    db = Depends(get_db) if DEPENDENCIES_AVAILABLE else None
):
    """
    Obtener el estado del chatbot.
    Requiere autenticación.
    """
    if not DEPENDENCIES_AVAILABLE:
        return {
            "model_available": False,
            "model_name": "N/A",
            "context_length": 0,
            "status": "unavailable",
            "error": "Dependencies not available"
        }

    try:
        model_available = await chatbot_service.is_model_available()
        return {
            "model_available": model_available,
            "model_name": chatbot_service.model_name,
            "context_length": chatbot_service.get_context_length(),
            "status": "available" if model_available else "unavailable"
        }
    except Exception as e:
        return {
            "model_available": False,
            "model_name": chatbot_service.model_name if chatbot_service else "N/A",
            "context_length": 0,
            "status": "error",
            "error": str(e)
        }