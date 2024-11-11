import os
import sys
import settings
import smtplib
# import ssl
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv
from decouple import config

if getattr(sys, 'frozen', False):
    # Si está corriendo como un ejecutable
    base_path = sys._MEIPASS
else:
    # Si está corriendo como un script en desarrollo
    base_path = os.path.abspath(".")

# Para acceder a los archivos en assets o upload:
assets_path = os.path.join(base_path, "assets")
# upload_path = os.path.join(base_path, "upload")

# Ejemplo de uso:
# icon_path = os.path.join(assets_path, "img", "parqueadero.png")

# if settings.tipo_app == 0:
#     path=os.path.join(os.getcwd(), "upload\\receipt\\")
# else:
#     path=os.path.join(os.getcwd(), "assets\\receipt\\")

load_dotenv()

# SENDER_EMAIL=os.getenv("EMAIL_USER")
# MAIL_PASSWORD=config("EMAIL_PASS")
SENDER_EMAIL=settings.email_user
MAIL_PASSWORD=settings.email_pass
RECEIVER_EMAIL=settings.correo_electronico

def send_mail_billing(SENDER_EMAIL, RECEIVER_EMAIL):
    consecutivo=str(settings.consecutivo2).zfill(6) if str(settings.consecutivo2[0:1]) == str(settings.prefijo[0:1]) else settings.consecutivo2
    documento="Factura de Venta" if str(consecutivo[0:1]) == str(settings.prefijo[0:1]) else "Recibo"
    msg=EmailMessage()
    msg["From"]=SENDER_EMAIL
    msg["To"]=RECEIVER_EMAIL
    msg["Subject"]=f"{documento + ' ' + consecutivo}"
    msg.set_content("Archivo adjunto...")
    msg.add_alternative(f"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">{documento + ' ' + consecutivo}</h1>
        </body>
    </html>
    """, subtype="html")

    file="receipt.pdf"

    # contexto=ssl.create_default_context()

    with open(f"{assets_path}\\receipt\\"+file, "rb") as f:
        file_data=f.read()
        # file_name=f.name
        file_name=documento + " " + consecutivo+Path(f.name).suffix

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # smtp.login(config("EMAIL_USER"), config("EMAIL_PASS"))
        # smtp.sendmail(config("EMAIL_USER"), RECEIVER_EMAIL, msg.as_string())
        smtp.login(settings.email_user, settings.email_pass)
        smtp.sendmail(settings.email_user, RECEIVER_EMAIL, msg.as_string())
        smtp.quit()

    settings.correo_electronico=""

def send_mail_user(SENDER_EMAIL, RECEIVER_EMAIL, token_password):    
    msg=EmailMessage()
    msg["From"]=SENDER_EMAIL
    msg["To"]=RECEIVER_EMAIL
    msg["Subject"]="Reestablecer contraseña"
    msg.set_content("Reestablecer contraseña")
    msg.add_alternative(f"""
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">Parqueadero</h1>
            <h3>Tu código de un solo uso es {token_password}</h3>
            <p>Ingresa en el programa de parqueadero con tu usuario ó correo electrónico y en la contraseña digita tu código de un solo uso. Luego en tu perfíl ingresa y confirma la nueva contraseña.</p>
        </body>
    </html>
    """, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # smtp.login(config("EMAIL_USER"), config("EMAIL_PASS"))
        # smtp.sendmail(config("EMAIL_USER"), RECEIVER_EMAIL, msg.as_string())
        smtp.login(settings.email_user, settings.email_pass)
        smtp.sendmail(settings.email_user, RECEIVER_EMAIL, msg.as_string())
        smtp.quit()

    settings.correo_electronico=""