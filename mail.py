import os
import settings
import smtplib
# import ssl
from pathlib import Path
from email.message import EmailMessage
# from dotenv import load_dotenv
from decouple import config

if settings.tipo_app == 0:
    path=os.path.join(os.getcwd(), "upload\\receipt\\")
else:
    path=os.path.join(os.getcwd(), "assets\\receipt\\")

# load_dotenv()

# SENDER_EMAIL=os.getenv("EMAIL_USER")
# MAIL_PASSWORD=os.getenv("EMAIL_PASS")
# RECEIVER_EMAIL="gjhg_69@hotmail.com"

# settings.prefijo="FE-"
# consecutivo="317000"

def send_mail_billing(SENDER_EMAIL, RECEIVER_EMAIL):
    consecutivo=str(settings.consecutivo2).zfill(7) if str(settings.consecutivo2[0:1]) == str(settings.prefijo[0:1]) else settings.consecutivo2
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

    with open(path+file, "rb") as f:
        file_data=f.read()
        # file_name=f.name
        file_name=documento + " " + consecutivo+Path(f.name).suffix

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(config("EMAIL_USER"), config("EMAIL_PASS"))
        smtp.sendmail(config("EMAIL_USER"), RECEIVER_EMAIL, msg.as_string())
        smtp.quit()

# send_mail_billing(SENDER_EMAIL, RECEIVER_EMAIL, MAIL_PASSWORD, consecutivo)