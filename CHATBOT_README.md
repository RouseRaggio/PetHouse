# 🤖 Chatbot IA con Ollama para PetHouse

Este documento explica cómo configurar y usar el chatbot de IA integrado con Ollama en PetHouse.

## 📋 Requisitos Previos

### 1. Instalar Ollama

**Windows:**
```bash
# Descarga desde: https://ollama.ai/download
# O usando winget:
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Descargar un Modelo de IA

Después de instalar Ollama, descarga un modelo compatible. Recomendamos:

```bash
# Modelo ligero y eficiente (recomendado)
ollama pull llama3.2

# Modelo más avanzado (requiere más recursos)
ollama pull llama3.1

# Ver modelos disponibles
ollama list
```

### 3. Verificar Instalación

```bash
# Verificar que Ollama está ejecutándose
ollama serve

# En otra terminal, probar el modelo
ollama run llama3.2
```

## 🚀 Configuración del Proyecto

### Backend

1. **Dependencias ya instaladas:**
   - `ollama` (cliente Python)
   - `requests`

2. **Archivos creados:**
   - `Backend/app/services/chatbot_service.py` - Servicio de Ollama
   - `Backend/app/routes/chatbot_routes.py` - Endpoints API
   - `Backend/app/main.py` - Router registrado

### Frontend

1. **Archivos creados:**
   - `Frontend/src/api/chatbot_service.js` - Cliente API
   - `Frontend/src/lib/components/Chatbot.svelte` - Modal del chat
   - `Frontend/src/lib/components/ChatbotFAB.svelte` - Botón flotante
   - `Frontend/src/routes/+layout.svelte` - Integración global

## 🎯 Uso del Chatbot

### Para Usuarios

1. **Inicia sesión** en PetHouse
2. **Haz clic** en el botón flotante 💬 en la esquina inferior derecha
3. **Escribe** tu mensaje sobre adopción, cuidado de mascotas, etc.
4. **Recibe** respuestas personalizadas del asistente IA

### Funcionalidades

- **Conversación contextual**: El chatbot recuerda la conversación
- **Limpieza de contexto**: Botón para reiniciar la conversación
- **Indicador de estado**: Muestra si el servicio está disponible
- **Animaciones amigables**: Interfaz cartoon consistente con PetHouse

## 🛠️ Personalización

### Cambiar el Modelo de IA

Edita `Backend/app/services/chatbot_service.py`:

```python
# Cambiar el modelo
chatbot_service = ChatbotService(model_name="llama3.1")
```

### Modificar el Prompt del Sistema

En `chatbot_service.py`, edita la función `initialize_context()`:

```python
system_prompt = """
Tu nuevo prompt personalizado aquí...
"""
```

### Cambiar la Apariencia

Edita los estilos en `Frontend/src/lib/components/Chatbot.svelte` para personalizar colores, tamaños, etc.

## 🔧 Solución de Problemas

### Error: "Model not available"

```bash
# Verificar que Ollama está ejecutándose
ollama serve

# Verificar que el modelo está descargado
ollama list

# Si no está descargado:
ollama pull llama3.2
```

### Error: "Connection refused"

- Verifica que el backend esté ejecutándose en `http://localhost:8000`
- Verifica que Ollama esté ejecutándose (`ollama serve`)

### Error: "401 Unauthorized"

- Asegúrate de estar logueado en PetHouse
- Verifica que el token JWT sea válido

### Rendimiento Lento

- Usa modelos más ligeros: `llama3.2` en lugar de `llama3.1`
- Reduce el `num_predict` en las opciones del modelo
- Aumenta la temperatura para respuestas más rápidas

## 📊 Endpoints API

### POST `/api/chatbot/chat`
Enviar mensaje al chatbot
```json
{
  "message": "Hola, ¿cómo adoptar una mascota?",
  "clear_context": false
}
```

### POST `/api/chatbot/clear`
Limpiar contexto del chat

### GET `/api/chatbot/status`
Verificar estado del servicio

## 🎨 Diseño y UX

- **Consistencia visual**: El chatbot mantiene el estilo cartoon de PetHouse
- **Responsive**: Funciona en móvil y desktop
- **Accesibilidad**: Navegación por teclado, contraste adecuado
- **Feedback visual**: Indicadores de escritura, estados de conexión

## 🔮 Futuras Mejoras

- Soporte para múltiples conversaciones
- Historial de chats guardado en BD
- Integración con datos de mascotas específicas
- Respuestas multimedia (imágenes, links)
- Modo voz a texto

---

¡El chatbot está listo para ayudar a los usuarios de PetHouse! 🐾