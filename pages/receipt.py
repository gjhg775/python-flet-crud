import os
import locale
import qrcode
import datetime
import settings
import subprocess
import webbrowser
import pywhatkit
import win32api
import win32print
from fpdf import FPDF
# from datatable import valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro
from datatable import get_configuration, get_variables

title="Parqueadero"

locale.setlocale(locale.LC_ALL, "")

if settings.sw == 0:
    path=os.path.join(os.getcwd(), "upload\\receipt\\")
else:
    path=os.path.join(os.getcwd(), "assets\\receipt\\")

configuracion=get_configuration()

if configuracion != None:
    id=configuracion[0][0]
    parqueadero=configuracion[0][1]
    nit=configuracion[0][2]
    regimen=configuracion[0][3]
    direccion=configuracion[0][4]
    telefono=configuracion[0][5]
    servicio=configuracion[0][6]
    resolucion=configuracion[0][7]
    fecha_desde=configuracion[0][8]
    fecha_hasta=configuracion[0][9]
    autoriza_del=configuracion[0][10]
    autoriza_al=configuracion[0][11]
    consecutivo=configuracion[0][12]
    settings.preview_register=configuracion[0][13]
    vista_previa_registro=False if configuracion[0][13] == 0 else True
    settings.print_register_receipt=configuracion[0][14]
    imprimir_registro=False if configuracion[0][14] == 0 else True
    settings.preview_cash=configuracion[0][15]
    vista_previa_cuadre=False if configuracion[0][15] == 0 else True
    settings.print_cash_receipt=configuracion[0][16]
    imprimir_cuadre=False if configuracion[0][16] == 0 else True
    settings.printer=configuracion[0][17]
    impresora=configuracion[0][17]

def show_input(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas):
    nit="Nit " + nit
    regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    consecutivo="Recibo " + str(consecutivo)
    entrada=str(entrada)
    entrada=str(entrada[0:19])
    entrada=f"Entrada " + str(entradas)

    pdf=FPDF("P", "mm", (80, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.set_font("helvetica", "", size=20)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 35, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 49, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 63, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 77, telefono, align="C")
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 91, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20)
    consecutivo_w=pdf.get_string_width(consecutivo)
    pdf.set_x((doc_w - consecutivo_w) / 2)
    pdf.cell(consecutivo_w, 107, consecutivo, align="C")
    placas1=f"Placa {placas}"
    placas1_w=pdf.get_string_width(placas1)
    pdf.set_x((doc_w - placas1_w) / 2)
    pdf.cell(placas1_w, 125, placas1, align="C")
    pdf.set_font("helvetica", "", size=15)
    entrada_w=pdf.get_string_width(entrada)
    pdf.set_x((doc_w - entrada_w) / 2)
    pdf.cell(entrada_w, 142, entrada, align="C")
    pdf.set_font("helvetica", "", size=10)
    comentario1_w=pdf.get_string_width(comentario1)
    pdf.set_x((doc_w - comentario1_w) / 2)
    pdf.cell(comentario1_w, 157, comentario1, align="C")
    comentario2_w=pdf.get_string_width(comentario2)
    pdf.set_x((doc_w - comentario2_w) / 2)
    pdf.cell(comentario2_w, 164, comentario2, align="C")
    comentario3_w=pdf.get_string_width(comentario3)
    pdf.set_x((doc_w - comentario3_w) / 2)
    pdf.cell(comentario3_w, 171, comentario3, align="C")
    # pdf.set_font("helvetica", "", size=15)
    # pdf.cell(10, 155, "")
    img=qrcode.make(f"{placas}")
    pdf.image(img.get_image(), x=25, y=98, w=30, h=30)
    pdf.set_font("helvetica", "", size=15)
    # pdf.code39(f"*{placas}*", x=0, y=70, w=4, h=20)
    if vehiculo == "Moto":
        pdf.code39(f"*{placas}*", x=2, y=130, w=2, h=15)
    if vehiculo == "Carro":
        pdf.code39(f"*{placas}*", x=2, y=130, w=2, h=15)
    if vehiculo == "Otro":
        pdf.code39(f"*{placas}*", x=2, y=130, w=2, h=15)
    pdf.output(path+"receipt.pdf")

    if settings.sw == 0:
        if settings.preview_register == 1:
            subprocess.Popen([path+"receipt.pdf"], shell=True)
        if settings.print_register_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=path
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        webbrowser.open_new(path+"receipt.pdf")

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

def show_output(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, salida, tiempo, vlr_total, entradas, salidas):
    nit="Nit " + nit
    regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    consecutivo=str(consecutivo)
    formato=f"%Y-%m-%d %H:%M"
    entrada=str(entrada)
    salida=str(salida)
    entrada=str(entrada[0:16])
    salida=str(salida[0:16])
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
    # print(minutos)
    duracion="Tiempo hh:mm " + str(f'{horas:02}') + ":" + str(f'{minutos:02}')
    # duracion="Tiempo hh:mm " + str(f'{tiempos}')
    entrada=f"Entrada " + str(entradas)
    salida=f"Salida   " + str(salidas)

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
        tarifa="Tarifa Horas-Moto"
    if vehiculo == "Carro":
        valor=valor_hora_carro
        tarifa="Tarifa Horas-Carro"
    if vehiculo == "Otro":
        valor=valor_hora_otro
        tarifa="Tarifa Horas-Otro"

    if dias == 0 and int(horas) <= 4:
        if int(horas) == 0:
            total=valor
        else:
            valor_horas=valor*int(horas)
            if minutos == 0:
                valor_fraccion=0
            if minutos > 0 and minutos <= 15:
                valor_fraccion=valor/2
            if minutos > 15:
                valor_fraccion=valor
            total=valor_horas+valor_fraccion
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
        turno=dias/12
        turno=int(turno)
        # horas=dias-(turno*12)
        # horas=int(horas)
        horas=dias-horas
        if int(horas) < 0:
            horas=horas*(-1)
        if int(horas) > 4:
            turno=turno+1
        if vehiculo == "Moto":
            if turno > 1 and int(horas) <= 4:
                total=int(horas)*valor_hora_moto
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_moto/2
                if minutos > 15:
                    valor_fraccion=valor_hora_moto
                vlr_total=total+valor_fraccion+(valor_turno_moto*turno)
            else:
                horas=horas-(turno*12)
                total=int(horas)*valor_hora_moto
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_moto/2
                if minutos > 15:
                    valor_fraccion=valor_hora_moto
                vlr_total=total+valor_fraccion+valor_turno_moto
        if vehiculo == "Carro":
            if turno > 1 and int(horas) <= 4:
                total=int(horas)*valor_hora_carro
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_carro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_carro
                vlr_total=total+valor_fraccion+(valor_turno_carro*turno)
            else:
                horas=horas-(turno*12)
                total=int(horas)*valor_hora_carro
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_carro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_carro
                vlr_total=total+valor_fraccion+valor_turno_carro
        if vehiculo == "Otro":
            if turno > 1 and int(horas) <= 4:
                total=int(horas)*valor_hora_otro
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_otro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_otro
                vlr_total=total+valor_fraccion+(valor_turno_otro*turno)
            else:
                horas=horas-(turno*12)
                total=int(horas)*valor_hora_otro
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_otro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_otro
                vlr_total=total+valor_fraccion+valor_turno_otro

    pdf=FPDF("P", "mm", (80, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.set_font("helvetica", "", size=20)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 35, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 49, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 63, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 77, telefono, align="C")
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 91, servicio, align="C")
    pdf.set_font("helvetica", "B", size=15)
    factura="Factura Electrónica de Venta"
    factura_w=pdf.get_string_width(factura)
    pdf.set_x((doc_w - factura_w) / 2)
    pdf.cell(factura_w, 105, factura, align="C")
    pdf.set_font("helvetica", "B", size=20)
    consecutivo1=f"FE-{consecutivo}"
    consecutivo1_w=pdf.get_string_width(consecutivo1)
    pdf.set_x((doc_w - consecutivo1_w) / 2)
    pdf.cell(consecutivo1_w, 122, consecutivo1, align="C")
    placas1=f"Placa {placas}"
    placas1_w=pdf.get_string_width(placas1)
    pdf.set_x((doc_w - placas1_w) / 2)
    pdf.cell(placas1_w, 139, placas1, align="C")
    pdf.set_font("helvetica", "", size=15)
    entrada_w=pdf.get_string_width(entrada)
    pdf.set_x((doc_w - entrada_w) / 2)
    pdf.cell(entrada_w, 156, entrada, align="C")
    salida_w=pdf.get_string_width(salida)
    pdf.set_x((doc_w - salida_w) / 2)
    pdf.cell(salida_w, 170, salida, align="C")
    duracion_w=pdf.get_string_width(duracion)
    pdf.set_x((doc_w - duracion_w) / 2)
    pdf.cell(duracion_w, 184, duracion, align="C")
    tarifa_w=pdf.get_string_width(tarifa)
    pdf.set_x((doc_w - tarifa_w) / 2)
    pdf.cell(tarifa_w, 198, tarifa, align="C")
    valor=locale.currency(valor, grouping=True)
    valor="Valor Unidad " + str(valor) 
    valor_w=pdf.get_string_width(valor)
    pdf.set_x((doc_w - valor_w) / 2)
    pdf.cell(valor_w, 212, valor, align="C")
    vlr_total=locale.currency(vlr_total, grouping=True)
    vlr_total="Total " + str(vlr_total) 
    vlr_total_w=pdf.get_string_width(vlr_total)
    pdf.set_x((doc_w - vlr_total_w) / 2)
    pdf.cell(vlr_total_w, 226, vlr_total, align="C")
    # img=qrcode.make(f"{placas}")
    # pdf.image(img.get_image(), x=35, y=118, w=30, h=30)
    pdf.output(path+"receipt.pdf")

    if settings.sw == 0:
        if settings.preview_register == 1:
            subprocess.Popen([path+"receipt.pdf"], shell=True)
        if settings.print_register_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=path
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        webbrowser.open_new(path+"receipt.pdf")

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

def show_cash_register(parqueadero, nit, regimen, direccion, telefono, servicio, registros):
    nit="Nit " + nit
    regimen="Régimen " + regimen
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

    pdf=FPDF("P", "mm", (80, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.set_font("helvetica", "", size=20)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 35, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 49, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 63, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 77, telefono, align="C")
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 91, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20)
    titulo_w=pdf.get_string_width(titulo)
    pdf.set_x((doc_w - titulo_w) / 2)
    pdf.cell(titulo_w, 105, titulo, align="C")
    pdf.set_font("helvetica", "", size=15)
    registro_w=pdf.get_string_width(registro)
    pdf.set_x((doc_w - registro_w) / 2)
    pdf.cell(registro_w, 119, registro, align="C")
    pdf.set_font("helvetica", "", size=10)
    fecha_w=pdf.get_string_width(fecha)
    pdf.set_x((doc_w - fecha_w) / 2)
    pdf.cell(fecha_w, 133, fecha, align="C")
    pdf.set_font("helvetica", "", size=9)
    pos=133
    pagina=0
    contador=0
    efectivo=0
    for registro in registros:
        pos+=10
        pagina+=1
        contador+=1
        consecutivo=registro[0]
        placa=registro[1]
        entrada=registro[2]
        salida=registro[3]
        vehiculo=registro[4]
        entrada=entrada.split(" ")
        entrada=str(entrada[1])
        salida=salida.split(" ")
        salida=str(salida[1])
        facturacion="Horas" if registro[5] == 0 else "Turnos"
        valor=locale.currency(registro[6], grouping=True)
        total=locale.currency(registro[8], grouping=True)
        row=consecutivo + "  " + placa + "  " + entrada + "  " + salida
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        pos+=10
        row=vehiculo + "  " + facturacion + "  " + str(valor) + "  " + str(total)
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        # pdf.cell(1, pos, row, align="R")
        efectivo+=registro[8]
        if pagina > 0 and contador == 6:
            pdf.add_page(same=True)
            pos=0
        if (contador%18) == 0:
            pdf.add_page(same=True)
            pos=0
    pdf.set_font("helvetica", "B", size=9)
    pos+=10
    efectivo=locale.currency(efectivo, grouping=True)
    efectivo="Total efectivo " + str(efectivo)
    # efectivo_w=pdf.get_string_width(efectivo)
    # pdf.set_x((doc_w - efectivo_w) / 2)
    # pdf.cell(efectivo_w, pos, efectivo, align="C")
    pdf.cell(0, pos, efectivo, align="R")
    pdf.output(path+"cash_register.pdf")

    if settings.sw == 0:
        if settings.preview_cash == 1:
            subprocess.Popen([path+"cash_register.pdf"], shell=True)
        if settings.print_cash_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=path
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        webbrowser.open_new(path+"cash_register.pdf")

def show_cash_register2(parqueadero, nit, regimen, direccion, telefono, servicio, registros):
    nit="Nit " + nit
    regimen="Régimen " + regimen
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

    pdf=FPDF("P", "mm", (80, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.set_font("helvetica", "", size=20)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15)
    nit_w=pdf.get_string_width(nit)
    pdf.set_x((doc_w - nit_w) / 2)
    pdf.cell(nit_w, 35, nit, align="C")
    regimen_w=pdf.get_string_width(regimen)
    pdf.set_x((doc_w - regimen_w) / 2)
    pdf.cell(regimen_w, 49, regimen, align="C")
    direccion_w=pdf.get_string_width(direccion)
    pdf.set_x((doc_w - direccion_w) / 2)
    pdf.cell(direccion_w, 63, direccion, align="C")
    telefono_w=pdf.get_string_width(telefono)
    pdf.set_x((doc_w - telefono_w) / 2)
    pdf.cell(telefono_w, 77, telefono, align="C")
    servicio_w=pdf.get_string_width(servicio)
    pdf.set_x((doc_w - servicio_w) / 2)
    pdf.cell(servicio_w, 91, servicio, align="C")
    pdf.set_font("helvetica", "B", size=20)
    titulo_w=pdf.get_string_width(titulo)
    pdf.set_x((doc_w - titulo_w) / 2)
    pdf.cell(titulo_w, 105, titulo, align="C")
    pdf.set_font("helvetica", "", size=15)
    registro_w=pdf.get_string_width(registro)
    pdf.set_x((doc_w - registro_w) / 2)
    pdf.cell(registro_w, 119, registro, align="C")
    pdf.set_font("helvetica", "", size=10)
    fecha_w=pdf.get_string_width(fecha)
    pdf.set_x((doc_w - fecha_w) / 2)
    pdf.cell(fecha_w, 133, fecha, align="C")
    pdf.set_font("helvetica", "", size=9)
    pos=133
    contador=0
    pendiente=0
    for registro in registros:
        pos+=10
        contador+=1
        pendiente+=1
        consecutivo=registro[0]
        placa=registro[1]
        entrada=registro[2]
        vehiculo=registro[4]
        entrada=entrada.split(" ")
        entrada=str(entrada[1])
        facturacion="Horas" if registro[5] == 0 else "Turnos"
        valor=locale.currency(registro[6], grouping=True)
        row=consecutivo + "  " + placa + "  " + entrada + "  " + vehiculo + "  " + facturacion + "  " + valor
        row_w=pdf.get_string_width(row)
        pdf.set_x((doc_w - row_w) / 2)
        pdf.cell(row_w, pos, row, align="C")
        if contador == 13:
            pdf.add_page(same=True)
            pos=0
    pdf.set_font("helvetica", "B", size=9)
    pos+=10
    pendiente="Total pendiente " + str(pendiente)
    pendiente_w=pdf.get_string_width(pendiente)
    pdf.set_x((doc_w - pendiente_w) / 2)
    pdf.cell(pendiente_w, pos, pendiente, align="C")
    pdf.output(path+"cash_register2.pdf")

    if settings.sw == 0:
        if settings.preview_cash == 1:
            subprocess.Popen([path+"cash_register2.pdf"], shell=True)
        if settings.print_cash_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile=path
            win32api.ShellExecute(
                0,
                "open",
                gsprint,
                '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
                '.',
                0
            )
    else:
        webbrowser.open_new(path+"cash_register2.pdf")
