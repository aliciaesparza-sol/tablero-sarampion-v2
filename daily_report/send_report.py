import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

# ----------------------------------------
# Configuration (replace placeholders)
# ----------------------------------------
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))  # 587 for TLS, 465 for SSL
SMTP_USER = os.getenv('SMTP_USER', 'your_email@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_password')
USE_SSL = os.getenv('SMTP_USE_SSL', 'false').lower() == 'true'

# List of recipients (change as needed)
RECIPIENTS = [
    "alicia.esparza@ssdurango.gob.mx",
    "alcantar.sarai20@gmail.com",
    "citlalis@hotmail.com",
    "karina.acosta@ssdurango.gob.mx",
    "maxiarreolav@gmail.com",
    "s.ramirez.s@gmail.com",
]

# Email details
SUBJECT = "Informe diario"
BODY = "Adjunto el informe diario.\nSaludos,\n[Tu Nombre]"

# Path to the report file to attach (replace with actual path)
REPORT_PATH = Path(os.getenv('REPORT_PATH', r'C:\path\to\your\report.pdf'))

def create_message():
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)

    if REPORT_PATH.is_file():
        with open(REPORT_PATH, "rb") as f:
            data = f.read()
            maintype, subtype = ("application", "pdf") if REPORT_PATH.suffix.lower() == ".pdf" else ("application", "octet-stream")
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=REPORT_PATH.name)
    else:
        print(f"[WARN] Report file not found: {REPORT_PATH}")
    return msg

def send_email():
    msg = create_message()
    if USE_SSL:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    else:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    print("[INFO] Email sent successfully.")

if __name__ == "__main__":
    send_email()
