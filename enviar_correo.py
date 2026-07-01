# -*- coding: utf-8 -*-
import os
import json
import smtplib
import sys
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Forzar salida en UTF-8 para evitar problemas de codificación en consolas Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config_correo.json")

def cargar_configuracion():
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] No se encontró el archivo de configuración en: {CONFIG_PATH}")
        sys.exit(1)
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def enviar_correo():
    config = cargar_configuracion()
    
    smtp_server = config.get("smtp_server")
    smtp_port = config.get("smtp_port", 587)
    use_tls = config.get("use_tls", True)
    sender_email = config.get("sender_email")
    sender_password = config.get("sender_password")
    recipient_emails = config.get("recipient_emails", [])
    subject = config.get("email_subject", "Informe Diario")
    body = config.get("email_body", "Adjunto se encuentra el informe.")
    report_path = config.get("report_path")
    
    if not sender_email or not sender_password or not recipient_emails:
        print("[ERROR] Por favor configura 'sender_email', 'sender_password' y 'recipient_emails' en config_correo.json")
        sys.exit(1)
        
    print(f"📧 Preparando correo desde {sender_email} para {', '.join(recipient_emails)}...")
    
    # Crear mensaje MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = subject
    
    # Cuerpo del correo
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Adjuntar archivo si existe
    if report_path:
        if os.path.exists(report_path):
            filename = os.path.basename(report_path)
            print(f"📎 Adjuntando archivo: {filename} desde {report_path}")
            try:
                with open(report_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                # Utilizar codificación segura para nombres de archivo en cabeceras de email
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}"
                )
                msg.attach(part)
            except Exception as e:
                print(f"[ADVERTENCIA] No se pudo leer o adjuntar el archivo: {e}")
        else:
            print(f"[ADVERTENCIA] El archivo del informe no existe en la ruta configurada: {report_path}")
            print("El correo se enviará únicamente con el texto del mensaje.")

    # Conectar al servidor y enviar
    try:
        if use_tls:
            print(f"🔒 Conectando a {smtp_server}:{smtp_port} vía STARTTLS...")
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=15)
            server.ehlo()
            server.starttls() # Asegurar la conexión
            server.ehlo()
        else:
            print(f"🔒 Conectando a {smtp_server}:{smtp_port} vía SSL...")
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15)
            server.ehlo()
            
        print("🔐 Iniciando sesión...")
        server.login(sender_email, sender_password)
        
        print("✉️ Enviando correo...")
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        server.quit()
        print("✅ Correo electrónico enviado con éxito.")
    except Exception as e:
        print(f"[ERROR] Falló el envío de correo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    enviar_correo()
