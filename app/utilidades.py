
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from app import models
from app.config import get_current_user
from app.database import SessionLocal
from app.models import CorreoPromocional, RolEnum, Usuario
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv



def verificar_rol_requerido(roles_permitidos):
    if not isinstance(roles_permitidos, list):
        roles_permitidos = [roles_permitidos]

    def wrapper(current_user: models.Usuario = Depends(get_current_user)):
        if current_user.rol not in roles_permitidos:
            roles = ', '.join([r.value for r in roles_permitidos])
            raise HTTPException(status_code=403, detail=f"Acceso denegado. Se requiere rol: {roles}")
        return current_user
    return wrapper




load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def enviar_ticket(destinatario: str, venta_data: dict):
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Tu ticket de compra"
    mensaje["From"] = EMAIL_USER
    mensaje["To"] = destinatario

    # Construir cuerpo del ticket
    cuerpo = f"""
    <h3>Gracias por tu compra</h3>
    <p><strong>Producto:</strong> {venta_data['producto']}</p>
    <p><strong>Cantidad:</strong> {venta_data['cantidad']}</p>
    <p><strong>Total:</strong> ${venta_data['total']}</p>
    """

    mensaje.attach(MIMEText(cuerpo, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(EMAIL_USER, EMAIL_PASS)
        servidor.sendmail(EMAIL_USER, destinatario, mensaje.as_string())



