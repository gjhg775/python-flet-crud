import os
import locale
import qrcode
import subprocess
# import webbrowser
import bcrypt
import datetime
import settings
import sqlite3
import hashlib
import win32api
import win32print
from flet import *
from fpdf import FPDF

conn=sqlite3.connect('database/parqueadero.db',check_same_thread=False)

valor=0

title="Parqueadero"

locale.setlocale(locale.LC_ALL, "")

path="receipt.pdf"
# path="/receipt/receipt.pdf"

tbu = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("Usuario")),
		DataColumn(Text("Nombre")),
		# DataColumn(Text("Acción")),
	],
	rows=[]
)

tba = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("Programa")),
		DataColumn(Text("Acceso")),
		# DataColumn(Text("Acción")),
	],
	rows=[]
)

tb = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("Consecutivo")),
		DataColumn(Text("Placa")),
		DataColumn(Text("Entrada")),
		DataColumn(Text("Salida")),
        # DataColumn(Text("Vehiculo")),
        # DataColumn(Text("Valor")),
        # DataColumn(Text("Tiempo")),
        # DataColumn(Text("Total")),
        # DataColumn(Text("Cuadre")),
        # DataColumn(Text("Usuario")),
		# DataColumn(Text("Acción")),
	],
	rows=[]
)

tbc = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("Consecutivo")),
		DataColumn(Text("Placa")),
		DataColumn(Text("Entrada")),
		DataColumn(Text("Salida")),
        DataColumn(Text("Vehículo")),
        DataColumn(Text("Facturación")),
        DataColumn(Text("Valor"), numeric=True),
        DataColumn(Text("Total"), numeric=True),
        # DataColumn(Text("Cuadre")),
	],
	rows=[]
)

id_edit=Text()
vehiculo_edit=RadioGroup(content=Row([
    Radio(label="Moto", value="Moto"),
    Radio(label="Moto", value="Moto"),
    Radio(label="Otro", value="Otro")
]))

def selectUser(usuario, contrasena):
    hash=hashlib.sha256(contrasena.encode()).hexdigest()
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(usuario,)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        login_user=""
        login_password=""
        bln_login=False

        if registros != []:
            # print(registros[0])

            hashed=registros[0][2]

            if hash == hashed:
                bln_login=True
            else:
                bln_login=False
        else:
            login_user="Usuario no registrado"
        if bln_login == False:
            login_password="Contraseña inválida"
        return login_user, login_password, bln_login
    except Exception as e:
        print(e)

def add_user(usuario, hashed, nombre):
    try:
        cursor=conn.cursor()
        sql="""INSERT INTO usuarios (usuario, clave, nombre) VALUES (?, ?, ?)"""
        values=(f"{usuario}", f"{hashed}", f"{nombre}")
        cursor.execute(sql, values)
        conn.commit()

        user="Admin"
        sql=f"""SELECT * FROM accesos WHERE usuario = '{user}'"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        for registro in registros:
            acceso_usuario=0
            programa=registro[2]
            if programa == "Registro":
                acceso_usuario=1
            sql="""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES (?, ?, ?)"""
            values=(f"{usuario}", f"{programa}", f"{acceso_usuario}")
            cursor.execute(sql, values)
            conn.commit()
    except Exception as e:
        print(e)

def get_configuration():
    try:
        cursor=conn.cursor()
        sql="SELECT * FROM configuracion"
        cursor.execute(sql)
        configuracion=cursor.fetchall()

        if configuracion != []:
            return configuracion
    except Exception as e:
        print(e)

configuracion=get_configuration()

if configuracion != None:
    parqueadero=configuracion[0][1]
    nit=configuracion[0][2]
    regimen=configuracion[0][3]
    direccion=configuracion[0][4]
    telefono=configuracion[0][5]
    servicio=configuracion[0][6]
    consecutivo=configuracion[0][7]

def update_configuration(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, id):
    try:
        cursor=conn.cursor()
        sql=f"""UPDATE configuracion SET parqueadero = ?, nit = ?, regimen = ?, direccion = ?, telefono = ?, servicio = ?, consecutivo = ? WHERE configuracion_id = ?"""
        values=(f"{parqueadero}", f"{nit}", f"{regimen}", f"{direccion}", f"{telefono}", f"{servicio}", f"{consecutivo}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        message="Configuración actualizada satisfactoriamente"
        return message
    except Exception as e:
        print(e)

def get_variables():
    try:
        cursor=conn.cursor()
        sql="SELECT * FROM variables"
        cursor.execute(sql)
        variables=cursor.fetchall()

        if variables != []:
            return variables
    except Exception as e:
        print(e)

variables=get_variables()

if variables != None:
    valor_hora_moto=variables[0][1]
    valor_turno_moto=variables[0][2]
    valor_hora_carro=variables[0][3]
    valor_turno_carro=variables[0][4]
    valor_hora_otro=variables[0][5]
    valor_turno_otro=variables[0][6]

def update_variables(vlr_hora_moto, vlr_turno_moto, vlr_hora_carro, vlr_turno_carro, vlr_hora_otro, vlr_turno_otro, id):
    try:        
        cursor=conn.cursor()
        sql=f"""UPDATE variables SET vlr_hora_moto = ?, vlr_turno_moto = ?, vlr_hora_carro = ?, vlr_turno_carro = ?, vlr_hora_otro = ?, vlr_turno_otro = ? WHERE variable_id = ?"""
        values=(f"{vlr_hora_moto}", f"{vlr_turno_moto}", f"{vlr_hora_carro}", f"{vlr_turno_carro}", f"{vlr_hora_otro}", f"{vlr_turno_otro}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        message="Variables actualizadas satisfactoriamente"
        return message
    except Exception as e:
        print(e)

def update_register(vehiculo, consecutivo, id, valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro):
    usuario=settings.username["username"]
    
    try:
        salida=datetime.datetime.now()

        if vehiculo == "Moto":
            valor=valor_hora_moto
        if vehiculo == "Carro":
            valor=valor_hora_carro
        if vehiculo == "Otro":
            valor=valor_hora_otro

        cursor=conn.cursor()

        sql=f"""SELECT * FROM usuarios WHERE usuario = '{usuario}'"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        usuario=registros[0][3]

        sql=f"""UPDATE registro SET salida = ?, valor = ?, usuario = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{valor}", f"{usuario}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE registro_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        id=registros[0][0]
        placa=registros[0][2]
        entrada=registros[0][3]
        valor=registros[0][7]
        tiempo=((registros[0][12])/60)/60

        if int(tiempo) <= 4:
            if int(tiempo) == 0:
                total=valor
            else:
                valor_horas=valor*int(tiempo)
                if (((registros[0][12])/60) % 60) == 0:
                    valor_fraccion=0
                if ((registros[0][12])/60) % 60 > 0 and ((registros[0][12])/60) % 60 <= 15:
                    valor_fraccion=valor/2
                if (((registros[0][12])/60) % 60 > 15 and ((registros[0][12])/60) % 60 <= 30) or ((registros[0][12])/60) % 60 > 30:
                    valor_fraccion=valor
                total=valor_horas+valor_fraccion
            if vehiculo == "Moto":
                if total > valor_turno_moto:
                    total=valor_turno_moto
            if vehiculo == "Carro":
                if total > valor_turno_carro:
                    total=valor_turno_carro
            if vehiculo == "Otro":
                if total > valor_turno_otro:
                    total=valor_turno_otro
            facturacion=0
        else:
            if vehiculo == "Moto":
                total=valor_turno_moto
            if vehiculo == "Carro":
                total=valor_turno_carro
            if vehiculo == "Otro":
                total=valor_turno_otro
            if tiempo > 12:
                turno=tiempo/12
                turno=int(turno)
                horas=tiempo-(turno*12)
                horas=int(round(horas))
                if horas < 0:
                    horas=horas*(-1)
                if horas > 4:
                    turno=turno+1
                if vehiculo == "Moto":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*valor_hora_moto
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(valor_turno_moto*turno)
                    else:
                        total=valor_turno_moto*turno
                if vehiculo == "Carro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*valor_hora_carro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(valor_turno_carro*turno)
                    else:
                        total=valor_turno_carro*turno
                if vehiculo == "Otro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*valor_hora_otro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(valor_turno_otro*turno)
                    else:
                        total=valor_turno_otro*turno
            facturacion=1

        tiempo=int(tiempo)
        sql=f"""UPDATE registro SET salida = ?, facturacion = ?, valor = ?, tiempo = ?, total = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE registro_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        entradas=registros[0][12]
        salidas=registros[0][13]

        # sql="SELECT consecutivo FROM configuracion"
        # cursor.execute(sql)
        # registros=cursor.fetchall()

        # consecutivo=registros[0][0]

        # id=1
        # consecutivo+=1
        # sql=f"""UPDATE configuracion SET consecutivo = ? WHERE configuracion_id = ?"""
        # values=(f"{consecutivo}", f"{id}")
        # cursor.execute(sql, values)
        # conn.commit()

        # salida=salida.strftime('%d/%m/%Y %H:%M')
        comentario1=""
        comentario2=""
        comentario3=""

        return consecutivo, vehiculo, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, entradas, salidas
    except Exception as e:
        print(e)

def add_register(vehiculo, placa):
    entrada=datetime.datetime.now()
    salida=entrada
    vehiculo=vehiculo

    if vehiculo == "Moto":
        valor=valor_hora_moto
    if vehiculo == "Carro":
        valor=valor_hora_carro
    if vehiculo == "Otro":
        valor=valor_hora_otro

    facturacion=0
    tiempo=0
    total=0
    cuadre=0
    usuario=settings.username["username"]

    try:
        cursor=conn.cursor()

        sql=f"""SELECT * FROM usuarios WHERE usuario = '{usuario}'"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        usuario=registros[0][3]

        id=1
        sql=f"""SELECT consecutivo FROM configuracion WHERE configuracion_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        consecutivo=registros[0][0]

        sql=f"""INSERT INTO registro (consecutivo, placa, entrada, salida, vehiculo, facturacion, valor, tiempo, total, cuadre, usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{consecutivo}", f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{cuadre}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE placa = '{placa}' AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        entradas=registros[0][12]
        salidas=registros[0][13]

        id=1
        consecutivos=int(consecutivo)+1
        sql=f"""UPDATE configuracion SET consecutivo = ? WHERE configuracion_id = ?"""
        values=(f"{consecutivos}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        comentario1="Sin éste recibo no se entrega el automotor."
        comentario2="Después de retirado el automotor no se"
        comentario3="acepta reclamos."

        return consecutivo, vehiculo, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, entradas, salidas
    except Exception as e:
        print(e)

def selectRegister(vehiculo, placa):
    try:
        total=0
        cursor=conn.cursor()
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = {total}"""
        # sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f"{placa}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros == []:
            consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, entradas, salidas=add_register(vehiculo, placa)
        else:
            variables = get_variables()

            if variables != None:
                valor_hora_moto=variables[0][1]
                valor_turno_moto=variables[0][2]
                valor_hora_carro=variables[0][3]
                valor_turno_carro=variables[0][4]
                valor_hora_otro=variables[0][5]
                valor_turno_otro=variables[0][6]

            id=registros[0][0]
            consecutivo=registros[0][1]
            consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, entradas, salidas=update_register(vehiculo, consecutivo, id, valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro)
            if total == None:
                total=0
        return consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, entradas, salidas

        # cursor=conn.cursor()
        # sql=f"""SELECT *, (strftime("%s", salida) - strftime("%s", entrada))/60/60 AS tiempo, (strftime("%s", salida) - strftime("%s", entrada))/60/60 * valor AS total FROM registro"""
        # cursor.execute(sql)
        # registros=cursor.fetchall()

        # print(registros[0])
        # # print((registros[0][3] - registros[0][2])/60/60)
        # # print(((int(registros[0][3]) - int(registros[0][2]))/60/60) * registros[0][4])
    except Exception as e:
        print(e)

def showedit(e):
    # data_edit=e.control.data
    # id_edit=data_edit["id"]
    consecutivo=e.control.data["consecutivo"]
    try:
        cursor=conn.cursor()
        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE consecutivo = ?"""
        values=(f"{consecutivo}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        parqueadero=configuracion[0][1]
        nit=configuracion[0][2]
        regimen=configuracion[0][3]
        direccion=configuracion[0][4]
        telefono=configuracion[0][5]
        servicio=configuracion[0][6]

        placa=registros[0][2]
        entrada=registros[0][3]
        salida=registros[0][4]
        vehiculo=registros[0][5]
        valor=registros[0][7]
        tiempo=registros[0][8]
        vlr_total=registros[0][9]
        entradas=registros[0][12]
        salidas=registros[0][13]

        comentario1="Sin éste recibo no se entrega el automotor."
        comentario2="Después de retirado el automotor no se"
        comentario3="acepta reclamos."

        if vlr_total == 0:
            showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placa, entrada, comentario1, comentario2, comentario3, entradas)
        if vlr_total > 0:
            showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placa, entrada, salida, valor, tiempo, vlr_total, entradas, salidas)
    except Exception as e:
        print(e)

def showdelete(e):
    try:
        values=e.control.data
        cursor=conn.cursor()
        sql=f"""DELETE FROM registro WHERE registro_id = ?"""
        cursor.execute(sql, values)
        conn.commit()
        tb.rows.clear()
        selectRegisters()
        tb.update()
    except Exception as e:
        print(e)

def showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas):
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
    pdf.output(path)
    subprocess.Popen([path], shell=True)
    # webbrowser.open_new(path)

    ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
    gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
    cPrinter=win32print.GetDefaultPrinter()
    pdfFile="C:/receipt/receipt.pdf"
    win32api.ShellExecute(
        0,
        "open",
        gsprint,
        '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
        '.',
        0
    )

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

def showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, salida, valor, tiempo, vlr_total, entradas, salidas):
    nit="Nit " + nit
    regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    consecutivo="Recibo " + str(consecutivo)
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
        if int(tiempo) <= 4:
            tarifa="Tarifa Horas-Moto"
            valor=valor_hora_moto
        else:
            tarifa="Tarifa Turno-Moto"
            valor=valor_turno_moto
    if vehiculo == "Carro":
        if int(tiempo) <= 4:
            tarifa="Tarifa Horas-Carro"
            valor=valor_hora_carro
        else:
            tarifa="Tarifa Turno-Carro"
            valor=valor_turno_carro
    if vehiculo == "Otro":
        if int(tiempo) <= 4:
            tarifa="Tarifa Horas-Otro"
            valor=valor_hora_otro
        else:
            tarifa="Tarifa Turno-Otro"
            valor=valor_turno_otro

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
    salida_w=pdf.get_string_width(salida)
    pdf.set_x((doc_w - salida_w) / 2)
    pdf.cell(salida_w, 156, salida, align="C")
    duracion_w=pdf.get_string_width(duracion)
    pdf.set_x((doc_w - duracion_w) / 2)
    pdf.cell(duracion_w, 170, duracion, align="C")
    tarifa_w=pdf.get_string_width(tarifa)
    pdf.set_x((doc_w - tarifa_w) / 2)
    pdf.cell(tarifa_w, 184, tarifa, align="C")
    valor=locale.currency(valor, grouping=True)
    valor="Valor Unidad " + str(valor) 
    valor_w=pdf.get_string_width(valor)
    pdf.set_x((doc_w - valor_w) / 2)
    pdf.cell(valor_w, 198, valor, align="C")
    vlr_total=locale.currency(vlr_total, grouping=True)
    vlr_total="Total " + str(vlr_total) 
    vlr_total_w=pdf.get_string_width(vlr_total)
    pdf.set_x((doc_w - vlr_total_w) / 2)
    pdf.cell(vlr_total_w, 212, vlr_total, align="C")
    # img=qrcode.make(f"{placas}")
    # pdf.image(img.get_image(), x=35, y=118, w=30, h=30)
    pdf.output(path)
    subprocess.Popen([path], shell=True)
    # webbrowser.open_new(path)

    ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
    gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
    cPrinter=win32print.GetDefaultPrinter()
    pdfFile="C:/receipt/receipt.pdf"
    win32api.ShellExecute(
        0,
        "open",
        gsprint,
        '-ghostscript "' + ghostscript + '" -printer "' + cPrinter + '" ' + pdfFile,
        '.',
        0
    )

    # ahora=str(datetime.datetime.now())
    # ahora=ahora.split(" ")
    # ahora=ahora[1]
    # ahora=ahora.split(":")
    # hora=int(ahora[0])
    # minuto=int(ahora[1])
    # minuto+=1
    # pywhatkit.sendwhatmsg("+57", path, hora, minuto, 15, True, 2)

# def show_edit_access(e):
#     # data_edit=e.control.data
#     # id_edit=data_edit["id"]
#     usuario=e.control.data["usuario"]
#     try:
#         cursor=conn.cursor()
#         sql=f"""SELECT programa, acceso_usuario FROM accesos WHERE usuario = ?"""
#         values=(f"{usuario}",)
#         cursor.execute(sql, values)
#         registros=cursor.fetchall()
        
#         accesos_usuario=[acceso_usuario for acceso_usuario in registros]
#         settings.accesos_usuario=accesos_usuario
#     except Exception as e:
#         print(e)

def update_access(e):
    programa=e.control.data
    chk=e.control
    programa=programa["programa"]
    acceso_usuario=0 if chk.value == False else 1
    usuario=lblAccesos.value
    usuario=usuario.split(" ")
    usuario=usuario[1]
    cursor=conn.cursor()
    sql=f"""UPDATE accesos SET acceso_usuario = ? WHERE programa = ? AND usuario = ?"""
    values=(f"{acceso_usuario}", f"{programa}", f"{usuario}")
    cursor.execute(sql, values)
    conn.commit()

def show_edit_access(e):
    usuario=e.control.data["usuario"]
    cursor=conn.cursor()
    sql=f"""SELECT programa, acceso_usuario FROM accesos WHERE usuario = '{usuario}'"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["programa", "acceso_usuario"]
        result=[dict(zip(keys, values)) for values in registros]

        tba.rows.clear()

        for x in result:
            tba.rows.append(
                DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=do_nothing,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["programa"])),
                        # DataCell(Text(x["acceso_usuario"])),
                        # DataCell(Checkbox(label=x["programa"], value=False if x["acceso_usuario"] == 0 else True)),
                        DataCell(Checkbox(value=False if x["acceso_usuario"] == 0 else True, data=x, on_change=update_access)),
                        DataCell(Row([
                        	# IconButton(icon="create",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	# IconButton(icon="delete",icon_color="red",
                        	# 	data=x["id"],
                        	# 	on_click=showdelete
                        	# 	),
                            # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	])),
                    ],
                ),
            )
    lblAccesos.value="Accesos " + usuario
    lblAccesos.update()
    tblAccesos.update()
    # return registros

def selectUsers(search):
    user="Super Admin"
    cursor=conn.cursor()
    if settings.username["username"] == "Super Admin":
        if search == "":
            sql=f"""SELECT usuario, nombre FROM usuarios"""
        else:
            sql=f"""SELECT usuario, nombre FROM usuarios WHERE usuario LIKE '%{search}%' OR nombre LIKE '%{search}%'"""
    elif settings.username["username"] == "Admin":
        if search == "":
            sql=f"""SELECT usuarios.usuario, usuarios.nombre FROM usuarios WHERE usuarios.usuario <> '{user}'"""
        else:
            sql=f"""SELECT usuarios.usuario, usuarios.nombre FROM usuarios WHERE usuarios.usuario <> '{user}' AND (usuarios.usuario LIKE '%{search}%' OR usuarios.nombre LIKE '%{search}%')"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["usuario", "nombre"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tbu.rows.append(
                DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=show_edit_access,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["usuario"])),
                        DataCell(Text(x["nombre"])),
                        DataCell(Row([
                        	# IconButton(icon="create",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	# IconButton(icon="delete",icon_color="red",
                        	# 	data=x["id"],
                        	# 	on_click=showdelete
                        	# 	),
                            # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	])),
                    ],
                ),
            )
    return registros

def selectRegisters(search):
    cuadre=0
    cursor=conn.cursor()
    # sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, tiempo, total, cuadre, usuario FROM registro"""
    if search == "":
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida) FROM registro WHERE cuadre = {cuadre}"""
    else:
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida) FROM registro WHERE (consecutivo LIKE '%{search}%' OR placa LIKE '%{search}%') AND cuadre = {cuadre}"""

    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["consecutivo", "placa", "entrada", "salida"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tb.rows.append(
                DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=showedit,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["consecutivo"])),
                        DataCell(Text(x["placa"])),
                        DataCell(Text(x["entrada"])),
                        DataCell(Text(x["salida"])),
                        # DataCell(Text(x["vehiculo"])),
                        # DataCell(Text(x["valor"])),
                        # DataCell(Text(x["tiempo"])),
                        # DataCell(Text(x["total"])),
                        # DataCell(Text(x["cuadre"])),
                        # DataCell(Text(x["usuario"])),
                        DataCell(Row([
                        	# IconButton(icon="create",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	# IconButton(icon="delete",icon_color="red",
                        	# 	data=x["id"],
                        	# 	on_click=showdelete
                        	# 	),
                            # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	])),
                    ],
                ),
            )
    return registros

def do_nothing(e):
    pass

def selectCashRegister():
    cuadre=0
    cursor=conn.cursor()    
    # sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = 0 AND cuadre = 0"""
    sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE cuadre = {cuadre}"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != []:
        keys=["consecutivo", "placa", "entrada", "salida", "vehiculo", "facturacion", "valor", "tiempo", "total", "cuadre"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tbc.rows.append(
                DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=do_nothing,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["consecutivo"])),
                        DataCell(Text(x["placa"])),
                        DataCell(Text(x["entrada"])),
                        DataCell(Text(x["salida"])),
                        DataCell(Text(x["vehiculo"])),
                        DataCell(Text("Horas" if x["facturacion"] == 0 else "Turnos")),
                        DataCell(Text(locale.currency(x["valor"], grouping=True))),
                        DataCell(Text(locale.currency(x["total"], grouping=True))),
                        # DataCell(Text(x["cuadre"])),
                        DataCell(Row([
                        	# IconButton(icon="create",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	# IconButton(icon="delete",icon_color="red",
                        	# 	data=x["id"],
                        	# 	on_click=showdelete
                        	# 	),
                            # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	])),
                    ],
                ),
            )
    return registros

lblAccesos=Text("Accesos", theme_style=TextThemeStyle.HEADLINE_SMALL, width=300, text_align="left", color=colors.PRIMARY)

tblUsuarios = Column([
    Row([tbu], scroll="always")
], height=60)

tblAccesos = Column([
    Row([tba], scroll="auto")
], height=274)

tblRegistro = Column([
    Row([tb], scroll="always")
], height=60)

tblCuadre = Column([
    Row([tbc], scroll="always")
], height=60)