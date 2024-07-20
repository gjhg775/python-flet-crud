import os
import time
import locale
import qrcode
import subprocess
import webbrowser
import bcrypt
import datetime
import settings
import sqlite3
import hashlib
import win32api
import win32print
from flet import *
from fpdf import FPDF
from pathlib import Path

conn=sqlite3.connect('database/parqueadero.db',check_same_thread=False)

valor=0

title="Parqueadero"

locale.setlocale(locale.LC_ALL, "")

if settings.sw == 0:
    path=os.path.join(os.getcwd(), "upload\\receipt\\")
else:
    path=os.path.join(os.getcwd(), "assets\\receipt\\")

tbu = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("Usuario")),
		DataColumn(Text("Nombre")),
		DataColumn(Text("Acción")),
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
        DataColumn(Text("Total"), visible=False),
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

# tbe = DataTable(
#     bgcolor=colors.PRIMARY_CONTAINER,
#     # bgcolor="#FFFFFF",
#     # border_radius=10,
#     # data_row_color={"hovered": "#e5eff5"},
# 	columns=[
# 		DataColumn(Text("Consecutivo")),
# 		DataColumn(Text("Placa")),
# 		DataColumn(Text("Entrada")),
# 		DataColumn(Text("Salida")),
#         DataColumn(Text("Vehículo")),
#         DataColumn(Text("Valor"), numeric=True),
#         DataColumn(Text("Tiempo"), numeric=True),
#         DataColumn(Text("Total"), numeric=True),
#         # DataColumn(Text("Cuadre")),
# 	],
# 	rows=[]
# )

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
        values=(f'{usuario}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        login_user=""
        login_password=""
        login_nombre=""
        login_photo=""
        bln_login=False

        if registros != []:
            # print(registros[0])

            hashed=registros[0][2]

            if hash == hashed:
                login_nombre=registros[0][3]
                login_photo=registros[0][4]
                bln_login=True
            else:
                bln_login=False
        else:
            login_user="Usuario no registrado"
        if bln_login == False:
            login_password="Contraseña inválida"
        return login_user, login_password, login_nombre, login_photo, bln_login
    except Exception as e:
        print(e)

def add_user(usuario, hashed, nombre, foto):
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(usuario,)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros != []:
            bln_login=False
            return bln_login

        sql="""INSERT INTO usuarios (usuario, clave, nombre, foto) VALUES (?, ?, ?, ?)"""
        values=(f"{usuario}", f"{hashed}", f"{nombre}", f"{foto}")
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

def update_user(usuario, foto):
    try:
        cursor=conn.cursor()
        sql="""UPDATE usuarios SET foto = ? WHERE usuario = ?"""
        values=(f"{foto}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()

        bgcolor="green"
        settings.message="Perfíl actualizado satisfactoriamente"
        settings.showMessage(bgcolor)
    except Exception as e:
        print(e)

def get_user(usuario):
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros != []:
            settings.photo=registros[0][4]
            # settings.photo=photo
            # settings.user_avatar.src=f"upload\\img\\{photo}"
            # settings.user_photo.src=f"upload\\img\\{photo}"
            # settings.user_avatar.update()
            # settings.user_photo.update()
            # settings.page.update()
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

def update_configuration(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vista_previa_registro, imprimir_registro, vista_previa_cuadre, imprimir_cuadre, impresora, id):
    try:
        cursor=conn.cursor()
        sql=f"""UPDATE configuracion SET parqueadero = ?, nit = ?, regimen = ?, direccion = ?, telefono = ?, servicio = ?, resolucion = ?, fecha_desde = ?, fecha_hasta = ?, autoriza_del = ?, autoriza_al = ?, consecutivo = ?, vista_previa_registro = ?, imprimir_registro = ?, vista_previa_cuadre = ?, imprimir_cuadre = ?, impresora = ? WHERE configuracion_id = ?"""
        values=(f"{parqueadero}", f"{nit}", f"{regimen}", f"{direccion}", f"{telefono}", f"{servicio}", f"{resolucion}", f"{fecha_desde}", f"{fecha_hasta}", f"{autoriza_del}", f"{autoriza_al}", f"{consecutivo}", f"{vista_previa_registro}", f"{imprimir_registro}", f"{vista_previa_cuadre}", f"{imprimir_cuadre}", f"{impresora}", f"{id}")
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
    # usuario=settings.username["username"]
    usuario=settings.username
    
    try:
        salida=datetime.datetime.now()
        formato=f"%Y-%m-%d %H:%M"
        salida=str(salida)
        salida=str(salida[0:16])
        salida=datetime.datetime.strptime(salida, formato)

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

        sql=f"""UPDATE registro SET salida = ?, valor = ?, retiro = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{valor}", f"{usuario}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE registro_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        id=registros[0][0]
        placa=registros[0][2]
        entrada=registros[0][3]
        salida=registros[0][4]
        valor=registros[0][7]
        # tiempo=((registros[0][13])/60)/60
        tiempo=registros[0][13]

        formato=f"%Y-%m-%d %H:%M"
        entrada=str(entrada)
        salida=str(salida)
        entrada=str(entrada[0:16])
        salida=str(salida[0:16])
        entrada=datetime.datetime.strptime(entrada, formato)
        salida=datetime.datetime.strptime(salida, formato)
        tiempos=salida - entrada
        dias=tiempos.days*24
        horas=tiempos.seconds//3600
        horas+=dias
        sobrante=tiempos.seconds%3600
        minutos=sobrante//60

        # segundos=registros[0][13]
        # dias=segundos//(24*60*60)
        # segundos=segundos % (24*60*60)
        # horas=segundos//(60*60)
        # segundos=segundos % (60*60)
        # minutos=segundos//60
        # segundos=segundos % 60

        # print("Días: {} Horas: {} Minutos: {} Segundos: {}".format(dias, horas, minutos, segundos))

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
            facturacion=0
        else:
            if vehiculo == "Moto":
                valor=valor_turno_moto
            if vehiculo == "Carro":
                valor=valor_turno_carro
            if vehiculo == "Otro":
                valor=valor_turno_otro
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
                    total=total+valor_fraccion+(valor_turno_moto*turno)
                else:
                    horas=horas-(turno*12)
                    total=int(horas)*valor_hora_moto
                    if minutos == 0:
                        valor_fraccion=0
                    if minutos > 0 and minutos <= 15:
                        valor_fraccion=valor_hora_moto/2
                    if minutos > 15:
                        valor_fraccion=valor_hora_moto
                    total=total+valor_fraccion+valor_turno_moto
            if vehiculo == "Carro":
                if turno > 1 and int(horas) <= 4:
                    total=int(horas)*valor_hora_carro
                    if minutos == 0:
                        valor_fraccion=0
                    if minutos > 0 and minutos <= 15:
                        valor_fraccion=valor_hora_carro/2
                    if minutos > 15:
                        valor_fraccion=valor_hora_carro
                    total=total+valor_fraccion+(valor_turno_carro*turno)
                else:
                    horas=horas-(turno*12)
                    total=int(horas)*valor_hora_carro
                    if minutos == 0:
                        valor_fraccion=0
                    if minutos > 0 and minutos <= 15:
                        valor_fraccion=valor_hora_carro/2
                    if minutos > 15:
                        valor_fraccion=valor_hora_carro
                    total=total+valor_fraccion+valor_turno_carro
            if vehiculo == "Otro":
                if turno > 1 and int(horas) <= 4:
                    total=int(horas)*valor_hora_otro
                    if minutos == 0:
                        valor_fraccion=0
                    if minutos > 0 and minutos <= 15:
                        valor_fraccion=valor_hora_otro/2
                    if minutos > 15:
                        valor_fraccion=valor_hora_otro
                    total=total+valor_fraccion+(valor_turno_otro*turno)
                else:
                    horas=horas-(turno*12)
                    total=int(horas)*valor_hora_otro
                    if minutos == 0:
                        valor_fraccion=0
                    if minutos > 0 and minutos <= 15:
                        valor_fraccion=valor_hora_otro/2
                    if minutos > 15:
                        valor_fraccion=valor_hora_otro
                    total=total+valor_fraccion+valor_turno_otro
            facturacion=1

        # tiempo=int(tiempo)
        sql=f"""UPDATE registro SET salida = ?, facturacion = ?, valor = ?, tiempo = ?, total = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE registro_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        entradas=registros[0][13]
        salidas=registros[0][14]

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
    formato=f"%Y-%m-%d %H:%M"
    entrada=str(entrada)
    entrada=str(entrada[0:16])
    entrada=datetime.datetime.strptime(entrada, formato)
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
    # usuario=settings.username["username"]
    usuario=settings.username

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

        sql=f"""INSERT INTO registro (consecutivo, placa, entrada, salida, vehiculo, facturacion, valor, tiempo, total, cuadre, ingreso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{consecutivo}", f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{cuadre}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE placa = '{placa}' AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        entradas=registros[0][13]
        salidas=registros[0][14]

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
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = ?"""
        # sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f"{placa}", f"{total}")
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
        resolucion=configuracion[0][7]
        fecha_desde=configuracion[0][8]
        fecha_hasta=configuracion[0][9]
        autoriza_del=configuracion[0][10]
        autoriza_al=configuracion[0][11]

        placa=registros[0][2]
        entrada=registros[0][3]
        salida=registros[0][4]
        vehiculo=registros[0][5]
        valor=registros[0][7]
        tiempo=registros[0][8]
        vlr_total=registros[0][9]
        entradas=registros[0][13]
        salidas=registros[0][14]

        comentario1="Sin éste recibo no se entrega el automotor."
        comentario2="Después de retirado el automotor no se"
        comentario3="acepta reclamos."

        if vlr_total == 0:
            showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placa, entrada, comentario1, comentario2, comentario3, entradas)
        if vlr_total > 0:
            showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placa, entrada, salida, valor, tiempo, vlr_total, entradas, salidas)
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
    pdf.output(path+"receipt.pdf")

    if settings.sw == 0:
        if settings.preview_register == 1:
            subprocess.Popen([path+"receipt.pdf"], shell=True)
        if settings.print_register_receipt == 1:
            ghostscript="C:\\GHOST\\GHOSTSCRIPTx64\\gs10031w64.exe"
            gsprint="C:\\GHOST\\GSPRINT\\gsprint.exe"
            # cPrinter=win32print.GetDefaultPrinter()
            cPrinter=settings.printer
            pdfFile="C:/receipt/receipt.pdf"
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

def showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placas, entrada, salida, valor, tiempo, vlr_total, entradas, salidas):
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
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_carro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_carro
                vlr_total=valor_fraccion+valor_turno_carro
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
                if minutos == 0:
                    valor_fraccion=0
                if minutos > 0 and minutos <= 15:
                    valor_fraccion=valor_hora_otro/2
                if minutos > 15:
                    valor_fraccion=valor_hora_otro
                vlr_total=valor_fraccion+valor_turno_otro

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
    pdf.cell(factura_w, 104, factura, align="C")
    pdf.set_font("helvetica", "B", size=20)
    consecutivo1=f"FE-{consecutivo}"
    consecutivo1_w=pdf.get_string_width(consecutivo1)
    pdf.set_x((doc_w - consecutivo1_w) / 2)
    pdf.cell(consecutivo1_w, 119, consecutivo1, align="C")
    pdf.set_font("helvetica", "", size=13)
    fecha_autoriza1="Desde " + str(fecha_desde) + " Hasta " + str(fecha_hasta)
    fecha_autoriza1_w=pdf.get_string_width(fecha_autoriza1)
    pdf.set_x((doc_w - fecha_autoriza1_w) / 2)
    pdf.cell(fecha_autoriza1_w, 132, fecha_autoriza1, align="C")
    autoriza1="Autoriza del " + str(autoriza_del) + " al " + str(autoriza_al)
    autoriza1_w=pdf.get_string_width(autoriza1)
    pdf.set_x((doc_w - autoriza1_w) / 2)
    pdf.cell(autoriza1_w, 144, autoriza1, align="C")
    resolucion1="Resolución " + str(resolucion)
    resolucion1_w=pdf.get_string_width(resolucion1)
    pdf.set_x((doc_w - resolucion1_w) / 2)
    pdf.cell(resolucion1_w, 156, resolucion1, align="C")
    pdf.set_font("helvetica", "B", size=20)
    placas1=f"Placa {placas}"
    placas1_w=pdf.get_string_width(placas1)
    pdf.set_x((doc_w - placas1_w) / 2)
    pdf.cell(placas1_w, 170, placas1, align="C")
    pdf.set_font("helvetica", "", size=15)
    entrada_w=pdf.get_string_width(entrada)
    pdf.set_x((doc_w - entrada_w) / 2)
    pdf.cell(entrada_w, 184, entrada, align="C")
    salida_w=pdf.get_string_width(salida)
    pdf.set_x((doc_w - salida_w) / 2)
    pdf.cell(salida_w, 198, salida, align="C")
    duracion_w=pdf.get_string_width(duracion)
    pdf.set_x((doc_w - duracion_w) / 2)
    pdf.cell(duracion_w, 212, duracion, align="C")
    tarifa_w=pdf.get_string_width(tarifa)
    pdf.set_x((doc_w - tarifa_w) / 2)
    pdf.cell(tarifa_w, 226, tarifa, align="C")
    valor=locale.currency(valor, grouping=True)
    valor="Valor Unidad " + str(valor) 
    valor_w=pdf.get_string_width(valor)
    pdf.set_x((doc_w - valor_w) / 2)
    pdf.cell(valor_w, 240, valor, align="C")
    vlr_total=locale.currency(vlr_total, grouping=True)
    vlr_total="Total " + str(vlr_total) 
    vlr_total_w=pdf.get_string_width(vlr_total)
    pdf.set_x((doc_w - vlr_total_w) / 2)
    pdf.cell(vlr_total_w, 254, vlr_total, align="C")
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
            pdfFile="C:/receipt/receipt.pdf"
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
    acceso=e.control.data
    chk=e.control
    usuario=lblAccesos.value
    usuario=usuario.split("Accesos ")
    usuario=usuario[1]
    if usuario != "Super Admin" and usuario != "Admin":
        programa=acceso["programa"]
        acceso_usuario=0 if chk.value == False else 1
        cursor=conn.cursor()
        sql=f"""UPDATE accesos SET acceso_usuario = ? WHERE programa = ? AND usuario = ?"""
        values=(f"{acceso_usuario}", f"{programa}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()

        # lblAccessUpdate.visible=True
        # lblAccessUpdate.update()
        # time.sleep(2)
        # lblAccessUpdate.visible=False
        # lblAccessUpdate.update()

        bgcolor="green"
        message="Registro actualizado satisfactoriamente"
        settings.message=message
        settings.showMessage(bgcolor)
    else:
        chk.value=not chk.value
        bgcolor="orange"
        message=f"Los accesos del usuario {usuario} no pueden ser modificados"
        settings.message=message
        settings.showMessage(bgcolor)

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
                    on_select_changed=lambda _: None,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["programa"])),
                        # DataCell(Text(x["acceso_usuario"])),
                        # DataCell(Checkbox(label=x["programa"], value=False if x["acceso_usuario"] == 0 else True)),
                        DataCell(Checkbox(value=False if x["acceso_usuario"] == 0 else True, data=x, on_change=update_access)),
                        # DataCell(Row([
                        #     # IconButton(icon="create",icon_color="blue",
                        #     # 	data=x,
                        #     # 	on_click=showedit
                        #     # 	),
                        #     # IconButton(icon="delete",icon_color="red",
                        #     # 	data=x["id"],
                        #     # 	on_click=showdelete
                        #     # 	),
                        #     # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        #     # 	data=x,
                        #     # 	on_click=showedit
                        #     # 	),
                        # ])),
                    ],
                ),
            )
    lblAccesos.value="Accesos " + usuario
    lblAccesos.update()
    tblAccesos.update()
    # return registros

def show_delete(e):
    settings.usuario=e.control.data
    usuario=settings.usuario
    title="Eliminar"
    message=f"Desea eliminar el usuario {usuario} ?"
    open_dlg_modal(e, title, message)        

def close_dlg(e):
    dlg_modal.open=False
    settings.page.update()

def open_dlg_modal(e, title, message):
    dlg_modal.title=Text(title, text_align="center")
    dlg_modal.content=Text(message, text_align="center")
    settings.page.dialog=dlg_modal
    dlg_modal.open=True
    settings.page.update()

def user_delete(usuario):
    dlg_modal.open=False
    settings.page.update()
    try:
        # usuario=e.control.data
        if usuario == "Super Admin" or usuario == "Admin":
            bgcolor="orange"
            settings.message=f"El usuario {usuario} no puede ser eliminado"
            settings.showMessage(bgcolor)
            return False
        
        get_user(usuario)
        
        cursor=conn.cursor()
        sql=f"""DELETE FROM accesos WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""DELETE FROM usuarios WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        conn.commit()
        tbu.rows.clear()
        tba.rows.clear()
        search=""
        selectUsers(search)
        lblAccesos.value="Accesos"
        lblAccesos.update()
        tblUsuarios.update()
        tblAccesos.update()

        if settings.photo != "default.jpg":
            os.remove(os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
        bgcolor="green"
        settings.message=f"Usuario {usuario} eliminado satisfactoriamente"
        settings.showMessage(bgcolor)
    except Exception as e:
        print(e)

def selectUsers(search):
    user="Super Admin"
    cursor=conn.cursor()
    # if settings.username["username"] == "Super Admin":
    if settings.username == "Super Admin":
        if search == "":
            sql=f"""SELECT usuario, nombre FROM usuarios"""
        else:
            sql=f"""SELECT usuario, nombre FROM usuarios WHERE usuario LIKE '%{search}%' OR nombre LIKE '%{search}%'"""
    # elif settings.username["username"] == "Admin":
    elif settings.username == "Admin":
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

        tbu.rows.clear()

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
                        	IconButton(icon="delete", icon_color="red",
                        		# data=x["id"],
                        		data=x["usuario"],
                        		on_click=show_delete
                        	),
                            # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        ])),
                    ],
                ),
            )
    return registros

def selectAccess(username):
    cursor=conn.cursor()
    sql=f"""SELECT programa, acceso_usuario FROM accesos WHERE usuario = '{username}'"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != []:
        settings.acceso_configuracion=registros[0][1]
        settings.acceso_variables=registros[1][1]
        settings.acceso_registro=registros[2][1]
        settings.acceso_cuadre=registros[3][1]
        settings.acceso_cierre=registros[4][1]

def selectRegisters(search):
    cuadre=0
    cursor=conn.cursor()
    # sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, tiempo, total, cuadre, usuario FROM registro"""
    if search == "":
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), total FROM registro WHERE cuadre = {cuadre}"""
    else:
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), total FROM registro WHERE (consecutivo LIKE '%{search}%' OR placa LIKE '%{search}%') AND cuadre = {cuadre}"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    tb.rows.clear()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["consecutivo", "placa", "entrada", "salida", "total"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            color=colors.GREEN_700 if x["total"] != 0 else None
            weight="bold" if x["total"] != 0 else None
            tb.rows.append(
                DataRow(
                    # color=colors.GREEN_100 if x["total"] != 0 else None,
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=showedit,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["consecutivo"], color=color, weight=weight)),
                        DataCell(Text(x["placa"], color=color, weight=weight)),
                        DataCell(Text(x["entrada"], color=color, weight=weight)),
                        DataCell(Text(x["salida"], color=color, weight=weight)),
                        # DataCell(Text(x["vehiculo"])),
                        # DataCell(Text(x["valor"])),
                        # DataCell(Text(x["tiempo"])),
                        DataCell(Text(x["total"], color=color, weight=weight)),
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
    # else:
    #     bgcolor="blue"
    #     message="No se encontraron registros"
    #     settings.message=message
    #     settings.showMessage(bgcolor)
    return registros

def exportRegister(fecha_desde, fecha_hasta):
    cuadre=1
    cursor=conn.cursor()
    if fecha_desde == "dd/mm/aaaa" and fecha_hasta == "dd/mm/aaaa":
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE cuadre = {cuadre}"""
    else:
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE salida BETWEEN '{fecha_desde}' AND '{fecha_hasta}' AND cuadre = {cuadre}"""
    cursor.execute(sql)
    registros=cursor.fetchall()
    return registros

def selectCashRegister():
    cuadre=0
    cursor=conn.cursor()    
    # sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = 0 AND cuadre = 0"""
    sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE cuadre = {cuadre}"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    tbc.rows.clear()

    if registros != []:
        keys=["consecutivo", "placa", "entrada", "salida", "vehiculo", "facturacion", "valor", "tiempo", "total", "cuadre"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            color=colors.GREEN_700 if x["total"] != 0 else None
            weight="bold" if x["total"] != 0 else None
            tbc.rows.append(
                DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=lambda _: None,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["consecutivo"], color=color, weight=weight)),
                        DataCell(Text(x["placa"], color=color, weight=weight)),
                        DataCell(Text(x["entrada"], color=color, weight=weight)),
                        DataCell(Text(x["salida"], color=color, weight=weight)),
                        DataCell(Text(x["vehiculo"], color=color, weight=weight)),
                        DataCell(Text("Horas" if x["facturacion"] == 0 else "Turnos", color=color, weight=weight)),
                        DataCell(Text(locale.currency(x["valor"], grouping=True), color=color, weight=weight)),
                        DataCell(Text(locale.currency(x["total"], grouping=True), color=color, weight=weight)),
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
    else:
        bgcolor="blue"
        message="No se encontraron registros"
        settings.message=message
        settings.showMessage(bgcolor)
    return registros

lblAccesos=Text("Accesos", theme_style=TextThemeStyle.HEADLINE_SMALL, text_align="left", color=colors.PRIMARY)

tblUsuarios = Column([
    Row([tbu], scroll="always")
], height=60, scroll="always")

tblAccesos = Column([
    Row([tba], scroll="always")
], height=300)

tblRegistro = Column([
    Row([tb], scroll="always")
], height=60)

tblCuadre = Column([
    Row([tbc], scroll="always")
], height=60)

dlg_modal=AlertDialog(
    bgcolor=colors.with_opacity(opacity=0.8, color=colors.PRIMARY_CONTAINER),
    modal=True,
    icon=Icon(name=icons.QUESTION_MARK, color=colors.with_opacity(opacity=0.8, color=colors.BLUE_900), size=50),
    # title=Text(title, text_align="center"),
    # content=Text(message, text_align="center"),
    actions=[
        TextButton("Sí", on_click=lambda _: user_delete(settings.usuario)),
        TextButton("No", autofocus=True, on_click=close_dlg)
    ],
    actions_alignment=MainAxisAlignment.END,
    # on_dismiss=lambda _: date_button.focus(),
)