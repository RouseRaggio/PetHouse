import json
from typing import List, Dict, Any
from fastapi import HTTPException
import logging

# Importación opcional de ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    ollama = None
    OLLAMA_AVAILABLE = False

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self, model_name: str = "llama3.2"):
        self.model_name = model_name
        self.context = []

    def initialize_context(self, system_prompt: str = None):
        """Inicializar el contexto del chat con un prompt del sistema"""
        if system_prompt is None:
            system_prompt = """
            Eres un asistente de IA amigable y útil para PetHouse, una plataforma de adopción de mascotas.

            Tu personalidad:
            - Eres cálido, amable y positivo
            - Te encanta hablar de mascotas y adopción
            - Das consejos útiles sobre cuidado de mascotas
            - Promueves la adopción responsable
            - Usas emojis apropiados (🐾, 🐶, 🐱, ❤️)
            - Mantienes respuestas concisas pero informativas

            Contexto de PetHouse:
            - Es una plataforma donde las personas pueden adoptar mascotas
            - Los dueños publican mascotas disponibles para adopción
            - Los adoptantes pueden ver perfiles de mascotas y contactar a los dueños
            - Hay un sistema de seguimiento GPS para mascotas adoptadas
            - Priorizamos el bienestar animal y la adopción responsable

            Responde en español de forma natural y conversacional.
            """

        self.context = [
            {
                'role': 'system',
                'content': system_prompt.strip()
            }
        ]

    def add_message(self, role: str, content: str):
        """Agregar un mensaje al contexto"""
        self.context.append({
            'role': role,
            'content': content
        })

        # Mantener solo los últimos 10 mensajes para no sobrecargar
        if len(self.context) > 11:  # 1 system + 10 conversaciones
            self.context = [self.context[0]] + self.context[-10:]

    async def generate_response(self, user_message: str) -> str:
        """Generar respuesta usando Ollama"""
        if not OLLAMA_AVAILABLE:
            return "Lo siento, el servicio de IA no está disponible en este momento. Por favor, instala Ollama y un modelo de IA. 🐾"

        try:
            # Agregar mensaje del usuario al contexto
            self.add_message('user', user_message)

            # Generar respuesta con Ollama
            response = await ollama.achat(
                model=self.model_name,
                messages=self.context,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'num_predict': 150,  # Limitar longitud de respuesta
                }
            )

            # Extraer respuesta
            ai_response = response['message']['content']

            # Agregar respuesta de IA al contexto
            self.add_message('assistant', ai_response)

            logger.info(f"Chatbot response generated for message: {user_message[:50]}...")
            return ai_response

        except Exception as e:
            logger.error(f"Error generating chatbot response: {str(e)}")
            # Fallback response en caso de error
            return "Lo siento, estoy teniendo dificultades técnicas. ¿Puedes intentar de nuevo? 🐾"

    def clear_context(self):
        """Limpiar el contexto del chat"""
        self.context = []
        self.initialize_context()

    def get_context_length(self) -> int:
        """Obtener el número de mensajes en el contexto"""
        return len(self.context)

    async def is_model_available(self) -> bool:
        """Verificar si el modelo está disponible"""
        if not OLLAMA_AVAILABLE:
            return False

        try:
            # Intentar hacer una petición simple
            response = await ollama.achat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': 'Hola'}],
                options={'num_predict': 1}
            )
            return True
        except Exception as e:
            logger.warning(f"Model {self.model_name} not available: {str(e)}")
            return False

# Instancia global del servicio
chatbot_service = ChatbotService()
chatbot_service.initialize_context()