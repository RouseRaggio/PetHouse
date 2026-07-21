# 🐾 PetHouse

Prototipo de plataforma web con inteligencia artificial.

## 📋 Descripción

PetHouse conecta a personas interesadas en adoptar con mascotas disponibles, e incorpora agentes de IA para acompañar todo el proceso: desde resolver dudas generales hasta dar seguimiento veterinario personalizado a cada mascota adoptada.

## ✨ Funcionalidades principales

- **Catálogo de mascotas disponibles** para adopción, con panel administrativo (dashboard, gráficos, reportes en PDF/CSV)
- **Chatbot general ("Togo")** para resolver dudas sobre adopción, funcionando con IA
- **Agente Veterinario IA**: tarjeta digital de la mascota, historial médico, recordatorios y seguimiento personalizado por mascota
- **Bot de Telegram con RAG** (en desarrollo): recordatorios automáticos de citas y cuidados, vinculado a cada usuario y mascota
- **Autenticación**: registro tradicional y Google OAuth
- **Panel de administración** con gestión de usuarios y mascotas, adopciones y auditoría

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|---|---|
| Frontend | Angular (PWA) |
| Backend | FastAPI (Python) |
| IA / LLM | Ollama + LLaMA 3.2 |
| Base de datos | PostgreSQL |
| Contenedores | Docker + Docker Compose |
| Hosting frontend | Vercel |
| Exposición de backend | en proceso |

## 📁 Estructura del repositorio

```
PetHouse/
├── Backend/              # API FastAPI + Docker Compose (FastAPI, Ollama, PostgreSQL)
│   └── docker-compose.yaml
├── FrontendV2/            # Aplicación Angular (PWA)
│   ├── src/
│   │   ├── app/
│   │   └── environments/
│   └── package.json
└── README.md
```
