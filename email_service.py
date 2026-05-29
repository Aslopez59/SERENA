import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SERENA_EMAIL = os.getenv("SERENA_EMAIL", "bienestarucca@gmail.com")
BIENESTAR_EMAIL = os.getenv("BIENESTAR_EMAIL", "bienestarucca@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SERENA_EMAIL_PASSWORD = os.getenv("SERENA_EMAIL_PASSWORD", "")


def enviar_correo(destinatario: str, asunto: str, contenido: str) -> bool:
    """Envía un correo real si el SMTP está configurado.
    Si no hay contraseña configurada, retorna False y el sistema sigue funcionando.
    """
    if not SERENA_EMAIL_PASSWORD:
        return False

    mensaje = EmailMessage()
    mensaje["From"] = SERENA_EMAIL
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(contenido)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SERENA_EMAIL, SERENA_EMAIL_PASSWORD)
        smtp.send_message(mensaje)

    return True
