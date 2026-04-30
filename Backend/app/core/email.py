import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def send_gps_email(user_email, user_name, imei):
    """
    Envía un correo electrónico al usuario notificando el envío del GPS.
    Requiere configurar SMTP_SERVER, SMTP_PORT, SMTP_USER y SMTP_PASSWORD en .env
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        print("--- AVISO: No se enviará correo real (Faltan credenciales en .env) ---")
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = user_email
    msg['Subject'] = "¡Tu Rastreador GPS de PetHouse ha sido enviado!"

    body = f"""
    Hola {user_name},

    ¡Tenemos excelentes noticias! Tu solicitud de rastreador GPS ha sido aprobada y el dispositivo ya va en camino.

    DETALLES DE TU DISPOSITIVO:
    - IMEI: {imei}

    ¿CÓMO RASTREAR?
    1. Inicia sesión en PetHouse.
    2. Ve a la sección 'Rastreador'.
    3. Ingresa el número de IMEI arriba mencionado en la plataforma integrada.

    Si tienes alguna duda, responde a este correo.

    Atentamente,
    El equipo de PetHouse
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, user_email, text)
        server.quit()
        print(f"--- Correo real enviado a {user_email} ---")
        return True
    except Exception as e:
        print(f"!!! ERROR CRÍTICO ENVIANDO CORREO: {type(e).__name__}: {e}")
        return False

def send_adoption_approval_email(user_email, user_name, pet_name):
    """
    Envía un correo electrónico al usuario notificando la aprobación de su adopción.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        print("--- AVISO: No se enviará correo real (Faltan credenciales en .env) ---")
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = user_email
    msg['Subject'] = f"¡Felicidades! Tu solicitud para adoptar a {pet_name} ha sido aprobada"

    body = f"""
    Hola {user_name},

    ¡Es un placer informarte que tu solicitud de adopción para {pet_name} ha sido APROBADA! 🎉

    Estamos muy felices de que {pet_name} haya encontrado un hogar responsable como el tuyo.

    PRÓXIMOS PASOS:
    1. Acércate a nuestra casa de adopción en los próximos 3 días hábiles.
    2. Trae tu documento de identidad original.
    3. Trae una correa o guacal según corresponda para transportar a tu nuevo mejor amigo.

    UBICACIÓN:
    Casa PetHouse - Barranquilla, Colombia.
    Horario: Lunes a Sábado, 8:00 AM - 5:00 PM.

    Si tienes alguna duda adicional, puedes responder a este correo o llamarnos.

    ¡Te esperamos con mucha emoción!

    Atentamente,
    El equipo de PetHouse
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(smtp_user, user_email, text)
        server.quit()
        print(f"--- Correo de adopción enviado a {user_email} ---")
        return True
    except Exception as e:
        print(f"!!! ERROR CRÍTICO ENVIANDO CORREO ADOPCIÓN: {type(e).__name__}: {e}")
        return False
