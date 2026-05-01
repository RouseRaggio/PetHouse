#!/usr/bin/env python3
"""
Script de verificación para Ollama y el chatbot de PetHouse
Ejecuta: python check_ollama.py
"""

import sys
import subprocess
import requests
import time

def check_ollama_running():
    """Verificar si Ollama está ejecutándose"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("[OK] Ollama esta instalado y ejecutandose")
            return True
        else:
            print("[ERROR] Ollama no esta ejecutandose")
            return False
    except FileNotFoundError:
        print("[ERROR] Ollama no esta instalado")
        return False
    except subprocess.TimeoutExpired:
        print("[WARNING] Ollama esta tardando en responder")
        return False

def check_ollama_models():
    """Verificar modelos disponibles"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        models = result.stdout.strip().split('\n')[1:]  # Saltar header

        if models and models[0].strip():
            print(f"[INFO] Modelos disponibles: {len(models)}")
            for model in models[:3]:  # Mostrar primeros 3
                if model.strip():
                    print(f"   - {model.split()[0]}")
            return True
        else:
            print("[ERROR] No hay modelos descargados")
            print("[TIP] Descarga un modelo con: ollama pull llama3.2")
            return False
    except Exception as e:
        print(f"[ERROR] Error verificando modelos: {e}")
        return False

def check_backend_running():
    """Verificar si el backend está ejecutándose"""
    try:
        response = requests.get('http://localhost:8000/docs', timeout=5)
        if response.status_code == 200:
            print("[OK] Backend de PetHouse esta ejecutandose")
            return True
        else:
            print(f"[ERROR] Backend responde con codigo {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("[ERROR] Backend no esta ejecutandose en http://localhost:8000")
        print("[TIP] Inicia el backend con: uvicorn app.main:app --reload")
        return False

def check_chatbot_endpoint():
    """Verificar si el endpoint del chatbot responde"""
    try:
        # Nota: Este endpoint requiere autenticación, así que solo verificamos que exista
        response = requests.options('http://localhost:8000/api/chatbot/status', timeout=5)
        if response.status_code in [200, 401, 405]:  # 401 es esperado (no autenticado)
            print("[OK] Endpoint del chatbot esta disponible")
            return True
        else:
            print(f"[ERROR] Endpoint del chatbot responde con {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("[ERROR] No se puede conectar al endpoint del chatbot")
        return False

def main():
    print("BOT Verificacion del Chatbot de PetHouse con Ollama")
    print("=" * 50)

    checks = [
        ("Ollama ejecutándose", check_ollama_running),
        ("Modelos disponibles", check_ollama_models),
        ("Backend ejecutándose", check_backend_running),
        ("Chatbot endpoint", check_chatbot_endpoint),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        print(f"\n[CHECK] Verificando: {name}")
        if check_func():
            passed += 1

    print("\n" + "=" * 50)
    print(f"[RESULT] Resultado: {passed}/{total} verificaciones pasaron")

    if passed == total:
        print("[SUCCESS] Todo esta listo! El chatbot deberia funcionar correctamente.")
        print("\n[TIP] Para probar:")
        print("   1. Inicia sesion en PetHouse")
        print("   2. Haz clic en el boton flotante (💬)")
        print("   3. Escribe un mensaje sobre mascotas")
    else:
        print("[WARNING] Algunos componentes no estan configurados correctamente.")
        print("\n[SOLUTIONS] Soluciones:")
        if not check_ollama_running():
            print("   - Instala Ollama desde: https://ollama.ai/download")
        if not check_ollama_models():
            print("   - Descarga un modelo: ollama pull llama3.2")
        if not check_backend_running():
            print("   - Inicia el backend: uvicorn app.main:app --reload")
        if not check_chatbot_endpoint():
            print("   - Verifica que las rutas esten registradas en main.py")

if __name__ == "__main__":
    main()