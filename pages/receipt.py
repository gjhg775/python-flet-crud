import os
import sys
import locale
import qrcode
import bcrypt
import datetime
import time
import settings
import subprocess
import webbrowser
import pywhatkit
import hashlib
import win32api
import win32print
from fpdf import FPDF
# from datatable import valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro
from datatable import get_configuration, get_variables
from dotenv import load_dotenv
from decouple import config

title="Parqueadero"

locale.setlocale(locale.LC_ALL, "")

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

configuracion=get_configuration()

if configuracion != None:
    id=configuracion[0][0]
    settings.parqueadero=configuracion[0][1]
    parqueadero=configuracion[0][1]
    nit=configuracion[0][2]
    regimen=configuracion[0][3]
    direccion=configuracion[0][4]
    telefono=configuracion[0][5]
    servicio=configuracion[0][6]
    settings.billing=configuracion[0][7]
    facturacion=False if configuracion[0][7] == 0 else True
    settings.resolucion=configuracion[0][8]
    resolucion=configuracion[0][8]
    settings.fecha_desde=configuracion[0][9]
    fecha_desde=configuracion[0][9]
    settings.fecha_hasta=configuracion[0][10]
    fecha_hasta=configuracion[0][10]
    settings.prefijo=configuracion[0][11]
    prefijo=configuracion[0][11]
    settings.autoriza_del=configuracion[0][12]
    autoriza_del=configuracion[0][12]
    settings.autoriza_al=configuracion[0][13]
    autoriza_al=configuracion[0][13]
    settings.clave_tecnica=configuracion[0][14]
    clave_tecnica=configuracion[0][14]
    settings.tipo_ambiente=configuracion[0][15]
    tipo_ambiente=configuracion[0][15]
    settings.cliente_final=configuracion[0][16]
    cliente=configuracion[0][16]
    settings.consecutivo=configuracion[0][17]
    consecutivo=configuracion[0][17]
    settings.preview_register=configuracion[0][18]
    vista_previa_registro=False if configuracion[0][18] == 0 else True
    settings.print_register_receipt=configuracion[0][19]
    imprimir_registro=False if configuracion[0][19] == 0 else True
    settings.send_email_register=configuracion[0][20]
    enviar_correo_electronico=False if configuracion[0][20] == 0 else True
    settings.email_user=configuracion[0][21]
    correo_usuario=configuracion[0][21]
    settings.email_pass=configuracion[0][22]
    correo_clave=configuracion[0][22]
    settings.secret_key=configuracion[0][23]
    secret_key=configuracion[0][23]
    settings.preview_cash=configuracion[0][24]
    vista_previa_cuadre=False if configuracion[0][24] == 0 else True
    settings.print_cash_receipt=configuracion[0][25]
    imprimir_cuadre=False if configuracion[0][25] == 0 else True
    settings.printer=configuracion[0][26]
    impresora=configuracion[0][26]
    settings.paper_width=configuracion[0][27]
    papel=configuracion[0][27]

def show_input(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    settings.consecutivo2=consecutivo
    # consecutivo=str(consecutivo).zfill(6) if str(consecutivo[0:1]) == str(settings.prefijo[0:1]) else str(consecutivo)
    consecutivo=str(consecutivo).zfill(6)
    consecutivo="Recibo " + consecutivo
    entrada=str(entrada)
    entrada=str(entrada[0:19])
    entrada=f"Entrada " + str(entradas)
    
    # pdf=FPDF("P", "mm", (int(str(settings.paper_width)[0:2]), 150))
    pdf=FPDF("P", "mm", (settings.paper_width, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.image(f"{assets_path}/img/logo_recibo.jpeg", x=4, y=2, w=20, h=20)
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    # pdf.set_x((doc_w - title_w) / 2)
    pdf.set_x(25)
    pdf.cell(title_w, 5, title, align="C")
    if len(parqueadero) <= 12:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    else:
        pdf.set_font("helvetica", "B", size=13)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 28, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 45, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 59, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 73, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 87, telefono, align="C")
    pdf.set_font("helvetica", "", size=14)
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 101, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    consecutivo_w=pdf.get_string_width(consecutivo)
    pdf.set_x((doc_w - consecutivo_w) / 2)
    pdf.cell(consecutivo_w, 117, consecutivo, align="C")
    placas1=f"Placa {placas}"
    placas1_w=pdf.get_string_width(placas1)
    pdf.set_x((doc_w - placas1_w) / 2)
    pdf.cell(placas1_w, 135, placas1, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    entrada_w=pdf.get_string_width(entrada)
    pdf.set_x((doc_w - entrada_w) / 2)
    pdf.cell(entrada_w, 152, entrada, align="C")
    pdf.set_font("helvetica", "", size=10 if settings.paper_width == 80 else 8)
    comentario1_w=pdf.get_string_width(comentario1)
    pdf.set_x((doc_w - comentario1_w) / 2)
    pdf.cell(comentario1_w, 167, comentario1, align="C")
    comentario2_w=pdf.get_string_width(comentario2)
    pdf.set_x((doc_w - comentario2_w) / 2)
    pdf.cell(comentario2_w, 174, comentario2, align="C")
    comentario3_w=pdf.get_string_width(comentario3)
    pdf.set_x((doc_w - comentario3_w) / 2)
    pdf.cell(comentario3_w, 181, comentario3, align="C")
    pdf.set_font("helvetica", "", size=15)
    # img=qrcode.make(f"{placas}")
    # pdf.image(img.get_image(), x=25 if int(str(settings.paper_width)[0:2]) == 80 else 14, y=98, w=30, h=30)
    pdf.set_font("helvetica", "", size=15)
    # pdf.code39(f"*{placas}*", x=0, y=70, w=4, h=20)
    if len(placas) == 5:
        pdf.code39(f"*{placas}*", x=12, y=107, w=1.5, h=5)
    elif len(placas) == 6:
        pdf.code39(f"*{placas}*", x=8, y=107, w=1.5, h=5)
    else:
        pdf.code39(f"*{placas}*", x=2, y=107, w=1.2, h=5)
    # if vehiculo == "Moto":
    #     # pdf.code39(f"*{placas}*", x=2, y=130, w=2, h=15)
    #     pdf.code39(f"*{placas}*", x=12, y=100, w=1.5, h=5)
    # if vehiculo == "Carro":
    #     pdf.code39(f"*{placas}*", x=12, y=100, w=1.5, h=5)
    # if vehiculo == "Otro":
    #     pdf.code39(f"*{placas}*", x=12, y=100, w=1.5, h=5)
    pdf.set_font("helvetica", "", size=8)
    impreso=os.getenv("FOOTER") if settings.billing == 1 and consecutivo[0:6] != "Recibo" else ""
    impreso_w=pdf.get_string_width(impreso)
    pdf.set_x((doc_w - impreso_w) / 2)
    pdf.set_y(120)
    pdf.write(0, impreso)
    pdf.output(f"{assets_path}\\receipt\\receipt.pdf")

    if settings.tipo_app == 0:
        if settings.preview_register == 1:
            subprocess.Popen([f"{assets_path}\\receipt\\receipt.pdf"], shell=True)
        if settings.print_register_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=f"{assets_path}\\receipt\\receipt.pdf"
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        if settings.preview_register == 1:
            webbrowser.open_new(f"{assets_path}\\receipt\\receipt.pdf")

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

def show_output(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, salida, tiempo, vlr_total, entradas, salidas):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    settings.consecutivo2=consecutivo
    # consecutivo=str(settings.consecutivo2).zfill(6) if str(settings.consecutivo2[0:1]) == str(settings.prefijo[0:1]) else str(settings.consecutivo2)
    consecutivo=str(consecutivo).zfill(6)

    if settings.tipo_app == 0:
        settings.billing = 0
        
    if settings.billing == 0:
        consecutivo="Recibo " + consecutivo
    else:
        consecutivo=settings.prefijo + str(consecutivo)
        settings.consecutivo2=consecutivo
    formato=f"%Y-%m-%d %H:%M:%S"
    entrada=str(entrada)
    salida=str(salida)
    fecha=str(salida[0:19])
    fecha=fecha.split(" ")
    generacion=fecha[0]
    hora=fecha[1]
    generacion=generacion.split("-")
    generacion=generacion[2] + "/" + generacion[1] + "/" + generacion[0] + " " + hora
    expedicion=generacion
    entrada=str(entrada[0:19])
    salida=str(salida[0:19])
    entrada=datetime.datetime.strptime(entrada, formato)
    salida=datetime.datetime.strptime(salida, formato)
    tiempos=salida - entrada
    # tiempos=str(tiempos)
    # tiempos=tiempos[0:len(tiempos)-3]
    # print(tiempos)
    dias=tiempos.days*24
    horas=tiempos.seconds//3600
    horas+=dias
    # print(horas)
    sobrante=tiempos.seconds%3600
    minutos=sobrante//60
    segundos=sobrante%60
    # print(minutos)
    duracion="Tiempo hh:mm:ss " + str(f'{horas:02}') + ":" + str(f'{minutos:02}') + ":" + str(f'{segundos:02}')
    # duracion="Tiempo hh:mm " + str(f'{tiempos}')
    entrada=f"Entrada " + str(entradas)
    salida=f"Salida   " + str(salidas)

    if settings.billing == 1:
        num_fac=consecutivo.split(settings.prefijo)
        num_fac=int(num_fac[1])
        # num_fac=consecutivo.split("-")
        # num_fac=int(num_fac[1])
        fec_fac=str(salidas).split("/")
        dia=fec_fac[0]
        mes=fec_fac[1]
        ano=fec_fac[2]
        ano=ano[0:4]
        fec_fac=ano+"-"+mes+"-"+dia
        hor_fac=str(salidas).split(" ")
        hor_fac=hor_fac[1] # Hora de la factura incluyendo GMT
        nit_fac=str(nit).split(" ")
        nit_fac=nit_fac[1]
        nit_fac=str(nit_fac).split("-")
        nit_fac=nit_fac[0]
        doc_adq=f"{settings.cliente_final}"
        val_fac=vlr_total
        val_fac2=f"{val_fac:.2f}"
        CodImp1=1
        CodImp1=f"{CodImp1:02}"
        ValImp1=0
        ValImp11=f"{ValImp1:.2f}"
        CodImp2=4
        CodImp2=f"{CodImp2:02}"
        ValImp2=0
        ValImp22=f"{ValImp2:.2f}"
        CodImp3=3
        CodImp3=f"{CodImp3:02}"
        ValImp3=0
        ValImp33=f"{ValImp3:.2f}"
        val_iva=0
        val_otro_im=0
        val_tol_fac=val_fac
        ValTot=val_fac+ValImp1+ValImp2+ValImp3
        ValTot2=f"{ValTot:.2f}"
        NitOFE=f"{nit_fac}"
        ClTec=f"{settings.clave_tecnica}"
        TipoAmbie=settings.tipo_ambiente
        TipoAmbie2=f"{TipoAmbie}"

        print(consecutivo)
        print(fec_fac)
        print(hor_fac)
        print(val_fac2)
        print(CodImp1)
        print(ValImp11)
        print(CodImp2)
        print(ValImp22)
        print(CodImp3)
        print(ValImp33)
        print(ValTot2)
        print(NitOFE)
        print(doc_adq)
        print(ClTec)
        print(TipoAmbie2)

        # cufe=f"{consecutivo}" + f"{fec_fac}" + f"{hor_fac}" + f"{val_fac:.2f}" + f"{CodImp1}" + f"{ValImp1:.2f}" + f"{CodImp2}" + f"{ValImp2:.2f}" + f"{CodImp3}" + f"{ValImp3:.2f}" + f"{ValTot:.2f}" + f"{NitOFE}" + f"{doc_adq}" + f"{ClTec}" + f"{TipoAmbie}"
        # cufe=consecutivo + fec_fac + hor_fac + f"{val_fac2:.2f}" + CodImp1 + f"{ValImp11:.2f}" + CodImp2 + f"{ValImp22:.2f}" + CodImp3 + f"{ValImp33:.2f}" + f"{ValTot2:.2f}" + NitOFE + doc_adq + ClTec + TipoAmbie2
        # cufe=consecutivo + fec_fac + hor_fac + val_fac2 + CodImp1 + ValImp11 + CodImp2 + ValImp22 + CodImp3 + ValImp33 + ValTot2 + NitOFE + doc_adq + ClTec + TipoAmbie2
        cufe=consecutivo + fec_fac + hor_fac + val_fac2 + CodImp1 + ValImp11 + CodImp2 + ValImp22 + CodImp3 + ValImp33 + ValTot2 + NitOFE + doc_adq + ClTec + TipoAmbie2
        # cufe=f"{consecutivo}{fec_fac}{hor_fac}{val_fac2}{CodImp1}{ValImp11}{CodImp2}{ValImp22}{CodImp3}{ValImp33}{ValTot2}{NitOFE}{doc_adq}{ClTec}{TipoAmbie2}"
        # cufe=cufe.encode("utf-8")
        # cufe=f"{consecutivo}{fec_fac}{hor_fac}{val_fac2}{CodImp1}{ValImp11}{CodImp2}{ValImp22}{CodImp3}{ValImp33}{ValTot2}{NitOFE}{doc_adq}{ClTec}{TipoAmbie2}"
        # hash=hashlib.sha384(cufe).hexdigest()
        bytes=cufe.encode("utf-8")
        hash=hashlib.sha384(bytes).hexdigest()
        cufe=hash

    variables=get_variables()

    if variables != None:
        valor_hora_moto=variables[0][1]
        valor_turno_moto=variables[0][2]
        valor_hora_carro=variables[0][3]
        valor_turno_carro=variables[0][4]
        valor_hora_otro=variables[0][5]
        valor_turno_otro=variables[0][6]

    if vehiculo == "Moto":
        valor=valor_hora_moto
        tarifa="Tarifa Hora-Moto"
    if vehiculo == "Carro":
        valor=valor_hora_carro
        tarifa="Tarifa Hora-Carro"
    if vehiculo == "Otro":
        valor=valor_hora_otro
        tarifa="Tarifa Hora-Otro"

    if dias == 0 and int(horas) <= 4:
        if int(horas) == 0:
            total=valor
        else:
            if vehiculo == "Moto":
                valor_turno=valor_turno_moto
                tarifa="Tarifa Turno-Moto"
            if vehiculo == "Carro":
                valor_turno=valor_turno_carro
                tarifa="Tarifa Turno-Carro"
            if vehiculo == "Otro":
                valor_turno=valor_turno_otro
                tarifa="Tarifa Turno-Otro"

            valor_horas=valor*int(horas)

            if int(horas) <=3:
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor/2
                if minutos > 15:
                    valor_fraccion=valor
                total=valor_horas+valor_fraccion
            else:
                total=valor_turno
    else:
        if vehiculo == "Moto":
            valor=valor_turno_moto
            tarifa="Tarifa Turno-Moto"
        if vehiculo == "Carro":
            valor=valor_turno_carro
            tarifa="Tarifa Turno-Carro"
        if vehiculo == "Otro":
            valor=valor_turno_otro
            tarifa="Tarifa Turno-Otro"
        # turno=dias/12
        turno=horas/12
        turno=int(turno)
        # horas=dias-(turno*12)
        # horas=int(horas)
        # horas=dias-horas
        horas=(turno*12)-horas
        if int(horas) < 0:
            horas=horas*(-1)
        incrementa=0
        if int(horas) > 3:
            turno=turno+1
            incrementa=1
        # horas=12-horas
        # if int(horas) < 0:
        #     horas=horas*(-1)
        valor_fraccion=0
        total=0
        if vehiculo == "Moto":
            if int(horas) <= 3:
                total=int(horas)*valor_hora_moto
            if incrementa == 0:
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_moto/2
                if minutos > 15:
                    valor_fraccion=valor_hora_moto
            vlr_total=total+valor_fraccion+(valor_turno_moto*turno)
        if vehiculo == "Carro":
            if int(horas) <= 3:
                total=int(horas)*valor_hora_carro
            if incrementa == 0:
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_carro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_carro
            vlr_total=total+valor_fraccion+(valor_turno_carro*turno)
        if vehiculo == "Otro":
            if int(horas) <= 3:
                total=int(horas)*valor_hora_otro
            if incrementa == 0:
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_otro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_otro
            vlr_total=total+valor_fraccion+(valor_turno_otro*turno)
    
    pdf=FPDF("P", "mm", (settings.paper_width, 150 if settings.billing == 0 else 255))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.image(f"{assets_path}/img/logo_recibo.jpeg", x=4, y=2, w=20, h=20)
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    # pdf.set_x((doc_w - title_w) / 2)
    pdf.set_x(25)
    pdf.cell(title_w, 5, title, align="C")
    if len(parqueadero) <= 12:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    else:
        pdf.set_font("helvetica", "B", size=13)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 28, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 45, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 59, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 73, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 87, telefono, align="C")
    pdf.set_font("helvetica", "", size=14)
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 101, servicio, align="C")
    if settings.billing == 1:
        pdf.set_font("helvetica", "B", size=14 if settings.paper_width == 80 else 11)
        factura="Factura Electrónica de Venta"
        factura_w=pdf.get_string_width(factura)
        pdf.set_x((doc_w - factura_w) / 2)
        pdf.cell(factura_w, 114, factura, align="C")
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        consecutivo1_w=pdf.get_string_width(consecutivo)
        pdf.set_x((doc_w - consecutivo1_w) / 2)
        pdf.cell(consecutivo1_w, 128, consecutivo, align="C")
        pdf.set_font("helvetica", "", size=12 if settings.paper_width == 80 else 10)
        fecha_autoriza1="Desde " + str(fecha_desde) + " Hasta " + str(fecha_hasta)
        fecha_autoriza1_w=pdf.get_string_width(fecha_autoriza1)
        pdf.set_x((doc_w - fecha_autoriza1_w) / 2)
        pdf.cell(fecha_autoriza1_w, 141, fecha_autoriza1, align="C")
        pdf.set_font("helvetica", "", size=13 if settings.paper_width == 80 else 11)
        autoriza1="Autoriza del " + str(autoriza_del) + " al " + str(autoriza_al)
        autoriza1_w=pdf.get_string_width(autoriza1)
        pdf.set_x((doc_w - autoriza1_w) / 2)
        pdf.cell(autoriza1_w, 153, autoriza1, align="C")
        resolucion1="Resolución " + str(resolucion)
        resolucion1_w=pdf.get_string_width(resolucion1)
        pdf.set_x((doc_w - resolucion1_w) / 2)
        pdf.cell(resolucion1_w, 165, resolucion1, align="C")
        forma_pago=f"Forma de Pago Contado"
        forma_pago_w=pdf.get_string_width(forma_pago)
        pdf.set_x((doc_w - forma_pago_w) / 2)
        pdf.cell(forma_pago_w, 178, forma_pago, align="C")
        pdf.set_font("helvetica", "", size=12 if settings.paper_width == 80 else 11)
        generacion=f"Fecha Generación " + generacion
        generacion_w=pdf.get_string_width(generacion)
        pdf.set_x((doc_w - generacion_w) / 2)
        pdf.cell(generacion_w, 191, generacion, align="C")
        expedicion=f"Fecha Expedición " + expedicion
        expedicion_w=pdf.get_string_width(expedicion)
        pdf.set_x((doc_w - expedicion_w) / 2)
        pdf.cell(expedicion_w, 203, expedicion, align="C")
        pdf.set_font("helvetica", "", size=13 if settings.paper_width == 80 else 11)
        cod_cliente=f"Cliente: {settings.cliente_final}"
        cod_cliente_w=pdf.get_string_width(cod_cliente)
        pdf.set_x((doc_w - cod_cliente_w) / 2)
        pdf.cell(cod_cliente_w, 216, cod_cliente, align="C")
        cliente=f"Consumidor Final"
        cliente_w=pdf.get_string_width(cliente)
        pdf.set_x((doc_w - cliente_w) / 2)
        pdf.cell(cliente_w, 228, cliente, align="C")
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        placas1=f"Placa {placas}"
        placas1_w=pdf.get_string_width(placas1)
        pdf.set_x((doc_w - placas1_w) / 2)
        pdf.cell(placas1_w, 243, placas1, align="C")
        pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
        entrada_w=pdf.get_string_width(entrada)
        pdf.set_x((doc_w - entrada_w) / 2)
        pdf.cell(entrada_w, 257, entrada, align="C")
        salida_w=pdf.get_string_width(salida)
        pdf.set_x((doc_w - salida_w) / 2)
        pdf.cell(salida_w, 270, salida, align="C")
        duracion_w=pdf.get_string_width(duracion)
        pdf.set_x((doc_w - duracion_w) / 2)
        pdf.cell(duracion_w, 285, duracion, align="C")
        tarifa_w=pdf.get_string_width(tarifa)
        pdf.set_x((doc_w - tarifa_w) / 2)
        pdf.cell(tarifa_w, 299, tarifa, align="C")
        valor=locale.currency(valor, grouping=True)
        valor="Valor Unidad " + str(valor) 
        valor_w=pdf.get_string_width(valor)
        pdf.set_x((doc_w - valor_w) / 2)
        pdf.cell(valor_w, 313, valor, align="C")
        vlr_total2=vlr_total
        vlr_total2=locale.currency(vlr_total2, grouping=True)
        vlr_total2="Total " + str(vlr_total2) 
        vlr_total2_w=pdf.get_string_width(vlr_total2)
        pdf.set_x((doc_w - vlr_total2_w) / 2)
        pdf.cell(vlr_total2_w, 327, vlr_total2, align="C")
        pdf.set_font("helvetica", "", size=13)
        title_cufe="CUFE:"
        title_cufe_w=pdf.get_string_width(title_cufe)
        pdf.set_x((doc_w - title_cufe_w) / 2)
        pdf.cell(title_cufe_w, 341, title_cufe, align="C")
        cufe_w=pdf.get_string_width(cufe)
        pdf.set_x((doc_w - cufe_w) / 2)
        pdf.set_y(185)
        pdf.write(0, cufe)
        img=qrcode.make(f"NumFac: {num_fac}\nFecFac: {fec_fac}\nHorFac: {hor_fac}\nNitFac: {nit_fac}\nDocAdq: {doc_adq}\nValFac: {val_fac:.2f}\nValIva: {val_iva:.2f}\nValOtroim: {val_otro_im:.2f}\nValTolFac: {val_tol_fac:.2f}\nCUFE: {cufe}")
        pdf.image(img.get_image(), x=26 if settings.paper_width == 80 else 14, y=206, w=25, h=25)
    else:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        consecutivo_w=pdf.get_string_width(consecutivo)
        pdf.set_x((doc_w - consecutivo_w) / 2)
        pdf.cell(consecutivo_w, 117, consecutivo, align="C")
        placas1=f"Placa {placas}"
        placas1_w=pdf.get_string_width(placas1)
        pdf.set_x((doc_w - placas1_w) / 2)
        pdf.cell(placas1_w, 135, placas1, align="C")
        pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
        entrada_w=pdf.get_string_width(entrada)
        pdf.set_x((doc_w - entrada_w) / 2)
        pdf.cell(entrada_w, 152, entrada, align="C")
        salida_w=pdf.get_string_width(salida)
        pdf.set_x((doc_w - salida_w) / 2)
        pdf.cell(salida_w, 166, salida, align="C")
        duracion_w=pdf.get_string_width(duracion)
        pdf.set_x((doc_w - duracion_w) / 2)
        pdf.cell(duracion_w, 180, duracion, align="C")
        tarifa_w=pdf.get_string_width(tarifa)
        pdf.set_x((doc_w - tarifa_w) / 2)
        pdf.cell(tarifa_w, 194, tarifa, align="C")
        valor=locale.currency(valor, grouping=True)
        valor="Valor Unidad " + str(valor) 
        valor_w=pdf.get_string_width(valor)
        pdf.set_x((doc_w - valor_w) / 2)
        pdf.cell(valor_w, 208, valor, align="C")
        vlr_total2=locale.currency(vlr_total, grouping=True)
        vlr_total2="Total " + str(vlr_total2) 
        vlr_total2_w=pdf.get_string_width(vlr_total2)
        pdf.set_x((doc_w - vlr_total2_w) / 2)
        pdf.cell(vlr_total2_w, 222, vlr_total2, align="C")
    pdf.set_font("helvetica", "", size=8)
    impreso=os.getenv("FOOTER") if settings.billing == 1 and consecutivo[0:6] != "Recibo" else ""
    impreso_w=pdf.get_string_width(impreso)
    pdf.set_x((doc_w - impreso_w) / 2)
    if settings.billing == 0:
        pdf.set_y(127)
    else:
        pdf.set_y(232)
    pdf.write(0, impreso)
    pdf.output(f"{assets_path}\\receipt\\receipt.pdf")

    if settings.tipo_app == 0:
        if settings.preview_register == 1:
            subprocess.Popen([f"{assets_path}\\receipt\\receipt.pdf"], shell=True)
        if settings.print_register_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=f"{assets_path}\\receipt\\receipt.pdf"
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        if settings.preview_register == 1:
            webbrowser.open_new(f"{assets_path}\\receipt\\receipt.pdf")

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

def show_cash_register(parqueadero, nit, regimen, direccion, telefono, servicio, registros):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    titulo="Reporte de Cuadre"
    registro="Registro Efectivo"
    fecha=datetime.datetime.now()
    fechahora=fecha.strftime('%d/%m/%Y %H:%M')
    fechahora=fechahora.split(" ")
    fecha=str(fechahora[0])
    hora=str(fechahora[1])
    fecha="Fecha " + fecha
    hora=" Hora " + hora
    fecha=fecha + hora

    pdf=FPDF("P", "mm", (settings.paper_width, 2000))
    # pdf=FPDF("P", "mm", (settings.paper_width, (25 * len(registros)) if contador < 6 else (15 * len(registros))))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.image(f"{assets_path}/img/logo_recibo.jpeg", x=4, y=2, w=20, h=20)
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    # pdf.set_x((doc_w - title_w) / 2)
    pdf.set_x(25)
    pdf.cell(title_w, 5, title, align="C")
    if len(parqueadero) <= 12:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    else:
        pdf.set_font("helvetica", "B", size=13)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 28, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 45, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 59, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 73, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 87, telefono, align="C")
    pdf.set_font("helvetica", "", size=14)
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 101, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20)
    titulo_w=pdf.get_string_width(titulo)
    pdf.set_x((doc_w - titulo_w) / 2)
    pdf.cell(titulo_w, 115, titulo, align="C")
    pdf.set_font("helvetica", "", size=15)
    registro_w=pdf.get_string_width(registro)
    pdf.set_x((doc_w - registro_w) / 2)
    pdf.cell(registro_w, 129, registro, align="C")
    pdf.set_font("helvetica", "", size=14)
    fecha_w=pdf.get_string_width(fecha)
    pdf.set_x((doc_w - fecha_w) / 2)
    pdf.cell(fecha_w, 144, fecha, align="C")
    pdf.set_font("helvetica", "", size=9)
    pos=146
    pagina=0
    contador=0
    efectivo=0
    for registro in registros:
        pos+=11
        pagina+=1
        contador+=1
        # consecutivo=settings.prefijo + str(registro[0]).zfill(6)
        consecutivo=str(registro[0]).zfill(6) if settings.billing == 0 else settings.prefijo + str(registro[0]).zfill(6)
        placa=registro[1]
        entrada=registro[2]
        salida=registro[3]
        vehiculo=registro[4]
        # entrada=entrada.split(" ")
        # entrada=str(entrada[1])
        # salida=salida.split(" ")
        # salida=str(salida[1])
        facturacion="Horas" if registro[5] == 0 else "Turnos"
        valor=locale.currency(registro[6], grouping=True)
        total=locale.currency(registro[8], grouping=True)
        pdf.set_font("helvetica", "", size=9 if settings.billing == 0 else 8)
        row=consecutivo + "  " + entrada + "  " + salida
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        pos+=10
        pdf.set_font("helvetica", "", size=9)
        row=placa + "  " + vehiculo + "  " + facturacion + "  " + str(valor) + "  " + str(total)
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        # pdf.cell(1, pos, row, align="R")
        efectivo+=registro[8]
        if pagina == 1 and contador == 6:
            pdf.add_page(same=True)
            contador=0
            pos=0
        # if (contador%18) == 0:
        # if contador == 6:
        #     pdf.add_page(same=True)
        #     contador=0
        #     pos=0
    pdf.set_font("helvetica", "B", size=9)
    pos+=10
    efectivo=locale.currency(efectivo, grouping=True)
    efectivo="Total efectivo " + str(efectivo)
    # efectivo_w=pdf.get_string_width(efectivo)
    # pdf.set_x((doc_w - efectivo_w) / 2)
    # pdf.cell(efectivo_w, pos, efectivo, align="C")
    pdf.cell(0, pos, efectivo, align="R")
    pdf.output(f"{assets_path}\\receipt\\cash_register.pdf")

    if settings.tipo_app == 0:
        if settings.preview_cash == 1:
            subprocess.Popen([f"{assets_path}\\receipt\\cash_register.pdf"], shell=True)
        if settings.print_cash_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=f"{assets_path}\\receipt\\cash_register.pdf"
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        if settings.preview_cash == 1:
            webbrowser.open_new(f"{assets_path}\\receipt\\cash_register.pdf")

def show_cash_register2(parqueadero, nit, regimen, direccion, telefono, servicio, registros):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    titulo="Reporte de Cuadre"
    registro="Registro Pendiente"
    fecha=datetime.datetime.now()
    fechahora=fecha.strftime('%d/%m/%Y %H:%M')
    fechahora=fechahora.split(" ")
    fecha=str(fechahora[0])
    hora=str(fechahora[1])
    fecha="Fecha " + fecha
    hora=" Hora " + hora
    fecha=fecha + hora
    
    pdf=FPDF("P", "mm", (settings.paper_width, 2000))
    # pdf=FPDF("P", "mm", (settings.paper_width, (25 * len(registros)) if len(registros) < 6 else (len(registros) * len(registros))))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.image(f"{assets_path}/img/logo_recibo.jpeg", x=4, y=2, w=20, h=20)
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    # pdf.set_x((doc_w - title_w) / 2)
    pdf.set_x(25)
    pdf.cell(title_w, 5, title, align="C")
    if len(parqueadero) <= 12:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    else:
        pdf.set_font("helvetica", "B", size=13)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 28, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 45, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 59, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 73, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 87, telefono, align="C")
    pdf.set_font("helvetica", "", size=14)
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 101, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20)
    titulo_w=pdf.get_string_width(titulo)
    pdf.set_x((doc_w - titulo_w) / 2)
    pdf.cell(titulo_w, 115, titulo, align="C")
    pdf.set_font("helvetica", "", size=15)
    registro_w=pdf.get_string_width(registro)
    pdf.set_x((doc_w - registro_w) / 2)
    pdf.cell(registro_w, 129, registro, align="C")
    pdf.set_font("helvetica", "", size=14)
    fecha_w=pdf.get_string_width(fecha)
    pdf.set_x((doc_w - fecha_w) / 2)
    pdf.cell(fecha_w, 144, fecha, align="C")
    pdf.set_font("helvetica", "", size=9)
    pos=146
    pagina=0
    contador=0
    pendiente=0
    for registro in registros:
        pos+=11
        pagina+=1
        contador+=1
        pendiente+=1
        # consecutivo=str(registro[0]) if settings.billing == 0 else str(registro[0]).zfill(6)
        consecutivo=str(registro[0]).zfill(6)
        placa=registro[1]
        entrada=registro[2]
        vehiculo=registro[4]
        # entrada=entrada.split(" ")
        # entrada=str(entrada[1])
        facturacion="Horas" if registro[5] == 0 else "Turnos"
        valor=locale.currency(registro[6], grouping=True)
        # row=consecutivo + "  " + placa + "  " + entrada + "  " + vehiculo + "  " + facturacion + "  " + valor
        # row_w=pdf.get_string_width(row)
        # pdf.set_x((doc_w - row_w) / 2)
        # pdf.cell(row_w, pos, row, align="C")
        row=consecutivo + "  " + entrada
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        pos+=10
        row=placa + "  " + vehiculo + "  " + facturacion + "  " + str(valor)
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        # if contador == 13:
        #     pdf.add_page(same=True)
        #     pos=0
    pdf.set_font("helvetica", "B", size=9)
    pos+=10
    pendiente="Total pendiente " + str(pendiente)
    pendiente_w=pdf.get_string_width(pendiente)
    pdf.set_x((doc_w - pendiente_w) / 2)
    pdf.cell(pendiente_w, pos, pendiente, align="C")
    pdf.output(f"{assets_path}\\receipt\\cash_register2.pdf")

    if settings.tipo_app == 0:
        if settings.preview_cash == 1:
            subprocess.Popen([f"{assets_path}\\receipt\\cash_register2.pdf"], shell=True)
        if settings.print_cash_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=f"{assets_path}\\receipt\\cash_register2.pdf"
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        if settings.preview_cash == 1:
            webbrowser.open_new(f"{assets_path}\\receipt\\cash_register2.pdf")
