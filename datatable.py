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
import random
from flet import *
from fpdf import FPDF
from pathlib import Path
from decouple import config
from mail import send_mail_billing

conn=sqlite3.connect('C:/pdb/database/parqueadero.db',check_same_thread=False)

valor=0

title="Parqueadero"

locale.setlocale(locale.LC_ALL, "")

if settings.tipo_app == 0:
    path=os.path.join(os.getcwd(), "upload\\receipt\\")
else:
    path=os.path.join(os.getcwd(), "assets\\receipt\\")

tbu = DataTable(
    bgcolor=colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
        DataColumn(Text("Foto")),
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
        # DataColumn(Text("Total"), visible=False),
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

def reset_password(usuario):
    try:
        cursor=conn.cursor()
        settings.token_password=random.randint(100000, 999999)
        hash=hashlib.sha256(str(settings.token_password).encode()).hexdigest()
        sql="""UPDATE usuarios SET clave = ? WHERE usuario = ? OR correo_electronico = ?"""
        values=(f'{hash}', f'{usuario}', f'{usuario}')
        cursor.execute(sql, values)
        conn.commit()

        sql="""SELECT * FROM usuarios WHERE usuario = ? OR correo_electronico = ? AND clave = ?"""
        values=(f'{usuario}', f'{usuario}', f'{hash}')
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        login_user=""

        if registros != []:
            correo_electronico=registros[0][2]
            password=registros[0][3]
        else:
            login_user="Usuario ó correo electrónico no registrado"
        return login_user, correo_electronico, password
    except Exception as e:
        print(e)

def selectUser(usuario, contrasena):
    hash=hashlib.sha256(str(contrasena).encode()).hexdigest()
    try:
        cursor=conn.cursor()
        sql="""SELECT * FROM usuarios WHERE usuario = ? OR correo_electronico = ?"""
        values=(f'{usuario}', f'{usuario}')
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        login_user=""
        correo_electronico=""
        login_password=""
        login_nombre=""
        login_photo=""
        bln_login=False

        if registros != []:
            hashed=registros[0][3]

            if hash == hashed:
                login_user=registros[0][1]
                correo_electronico=registros[0][2]
                login_password=registros[0][3]
                login_nombre=registros[0][4]
                login_photo=registros[0][5]
                bln_login=True
            else:
                bln_login=False
        else:
            login_user="Usuario ó correo electrónico no registrado"
        if bln_login == False:
            login_password="Contraseña inválida"
        return login_user, correo_electronico, login_password, login_nombre, login_photo, bln_login
    except Exception as e:
        print(e)

def add_user(usuario, correo_electronico, hashed, nombre, foto):
    try:
        cursor=conn.cursor()
        sql="""SELECT * FROM usuarios WHERE usuario = ? OR correo_electronico = ?"""
        values=(f'{usuario}', f'{usuario}')
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros != []:
            bln_login=False
            return bln_login

        sql="""INSERT INTO usuarios (usuario, correo_electronico, clave, nombre, foto) VALUES (?, ?, ?, ?, ?)"""
        values=(f"{usuario}", f"{correo_electronico}", f"{hashed}", f"{nombre}", f"{foto}")
        cursor.execute(sql, values)
        conn.commit()

        user="Admin"
        sql="""SELECT * FROM accesos WHERE usuario = ?"""
        values=(f'{user}',)
        cursor.execute(sql, values)
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

def update_user(usuario, clave, foto):
    hash=hashlib.sha256(clave.encode()).hexdigest()
    try:
        cursor=conn.cursor()
        sql="""UPDATE usuarios SET clave = ?, foto = ? WHERE usuario = ? OR correo_electronico = ?"""
        values=(f"{hash}", f"{foto}", f"{usuario}", f"{usuario}")
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
            settings.password=registros[0][3]
            settings.photo=registros[0][5]
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
    enviar_correo=False if configuracion[0][20] == 0 else True
    settings.preview_cash=configuracion[0][21]
    vista_previa_cuadre=False if configuracion[0][21] == 0 else True
    settings.print_cash_receipt=configuracion[0][22]
    imprimir_cuadre=False if configuracion[0][22] == 0 else True
    settings.printer=configuracion[0][23]
    impresora=configuracion[0][23]
    settings.paper_width=configuracion[0][24]
    papel=configuracion[0][24]

def update_configuration(parqueadero, nit, regimen, direccion, telefono, servicio, facturacion, resolucion, fecha_desde, fecha_hasta, prefijo, autoriza_del, autoriza_al, clave_tecnica, tipo_ambiente, cliente, consecutivo, vista_previa_registro, imprimir_registro, enviar_correo_electronico, vista_previa_cuadre, imprimir_cuadre, impresora, papel, id):
    try:
        cursor=conn.cursor()
        sql=f"""UPDATE configuracion SET parqueadero = ?, nit = ?, regimen = ?, direccion = ?, telefono = ?, servicio = ?, facturacion = ?, resolucion = ?, fecha_desde = ?, fecha_hasta = ?, prefijo = ?, autoriza_del = ?, autoriza_al = ?, clave_tecnica = ?, tipo_ambiente = ?, cliente = ?, consecutivo = ?, vista_previa_registro = ?, imprimir_registro = ?, enviar_correo_electronico = ?, vista_previa_cuadre = ?, imprimir_cuadre = ?, impresora = ?, papel = ? WHERE configuracion_id = ?"""
        values=(f"{parqueadero}", f"{nit}", f"{regimen}", f"{direccion}", f"{telefono}", f"{servicio}", f"{facturacion}", f"{resolucion}", f"{fecha_desde}", f"{fecha_hasta}", f"{prefijo}", f"{autoriza_del}", f"{autoriza_al}", f"{clave_tecnica}", f"{tipo_ambiente}", f"{cliente}", f"{consecutivo}", f"{vista_previa_registro}", f"{imprimir_registro}", f"{enviar_correo_electronico}", f"{vista_previa_cuadre}", f"{imprimir_cuadre}", f"{impresora}", f"{papel}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        # settings.billing=facturacion
        # settings.cliente_final=cliente
        # settings.printer=impresora
        # settings.paper_width=papel

        configuracion=get_configuration()

        if configuracion != None:
            id=configuracion[0][0]
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
            enviar_correo=False if configuracion[0][20] == 0 else True
            settings.preview_cash=configuracion[0][21]
            vista_previa_cuadre=False if configuracion[0][21] == 0 else True
            settings.print_cash_receipt=configuracion[0][22]
            imprimir_cuadre=False if configuracion[0][22] == 0 else True
            settings.printer=configuracion[0][23]
            impresora=configuracion[0][23]
            settings.paper_width=configuracion[0][24]
            papel=configuracion[0][24]
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

def update_register_mail(correo_electronico, placa):
    try:
        cursor=conn.cursor()
        sql=f"""UPDATE registro SET correo_electronico = ? WHERE placa = ?"""
        values=(f"{correo_electronico}", f"{placa}")
        cursor.execute(sql, values)
        conn.commit()
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

        sql=f"""SELECT entrada AS ent, datetime() AS sal FROM registro WHERE registro_id = ?"""
        values=(f"{id}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        ent=registros[0][0]
        sal=registros[0][1]

        settings.correcto=0

        if ent > sal:
            settings.correcto=1
            consecutivo=0
            vehiculo=""
            placa=""
            entrada=""
            salida=""
            tiempo=0
            comentario1=""
            comentario2=""
            comentario3=""
            total=0
            entradas=""
            salidas=""

        if settings.correcto == 0:
            sql="""SELECT * FROM usuarios WHERE usuario = ?"""
            values=(f'{usuario}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()

            usuario=registros[0][4]

            sql=f"""UPDATE registro SET salida = ?, valor = ?, retiro = ? WHERE registro_id = ?"""
            values=(f"{salida}", f"{valor}", f"{usuario}", f"{id}")
            cursor.execute(sql, values)
            conn.commit()

            sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE registro_id = ?"""
            values=(f'{id}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()

            id=registros[0][0]
            placa=registros[0][2]
            entrada=registros[0][3]
            salida=registros[0][4]
            valor=registros[0][7]
            # tiempo=((registros[0][13])/60)/60
            tiempo=registros[0][8]

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

            if dias == 0 and int(horas) <= 3:
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
                    total=total+valor_fraccion+(valor_turno_moto*turno)
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
                    total=total+valor_fraccion+(valor_turno_carro*turno)
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
                    total=total+valor_fraccion+(valor_turno_otro*turno)
                facturacion=1

            # tiempo=int(tiempo)
            sql="""UPDATE registro SET salida = ?, facturacion = ?, valor = ?, tiempo = ?, total = ? WHERE registro_id = ?"""
            values=(f"{salida}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{id}")
            cursor.execute(sql, values)
            conn.commit()

            sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE registro_id = ?"""
            values=(f'{id}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()

            correo_electronico=registros[0][13]
            entradas=registros[0][14]
            salidas=registros[0][15]

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

        return consecutivo, vehiculo, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas
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

        sql="""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(f'{usuario}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        usuario=registros[0][4]

        id=1
        sql="""SELECT consecutivo FROM configuracion WHERE configuracion_id = ?"""
        values=(f'{id}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        consecutivo=registros[0][0]
        correo_electronico=settings.correo_electronico

        sql=f"""INSERT INTO registro (consecutivo, placa, entrada, salida, vehiculo, facturacion, valor, tiempo, total, cuadre, ingreso, correo_electronico) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{consecutivo}", f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{cuadre}", f"{usuario}", f"{correo_electronico}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f'{placa}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        correo_electronico=registros[0][13]
        entradas=registros[0][14]
        salidas=registros[0][15]

        id=1
        consecutivos=int(consecutivo)+1
        sql=f"""UPDATE configuracion SET consecutivo = ? WHERE configuracion_id = ?"""
        values=(f"{consecutivos}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        comentario1="Sin éste recibo no se entrega el automotor."
        comentario2="Después de retirado el automotor no se"
        comentario3="aceptan reclamos."

        return consecutivo, vehiculo, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas
    except Exception as e:
        print(e)

def exist_email(placa):
    correo_electronico=""
    cursor=conn.cursor()
    sql=f"""SELECT * FROM registro WHERE placa = ? AND correo_electronico != ?"""
    values=(f"{placa}", f"{correo_electronico}")
    cursor.execute(sql, values)
    registros=cursor.fetchone()

    if registros != None:
        settings.correo_electronico=registros[13]

def selectRegister(vehiculo, placa):
    try:
        cursor=conn.cursor()
        total=0
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = ?"""
        # sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f"{placa}", f"{total}")
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros == []:
            consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas=add_register(vehiculo, placa)
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
            settings.consecutivo=registros[0][1]
            consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas=update_register(vehiculo, consecutivo, id, valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro)
            if total == None:
                total=0
        return consecutivo, vehiculos, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas

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
    settings.consecutivo2=consecutivo
    try:
        cursor=conn.cursor()
        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M', entrada) AS entradas, strftime('%d/%m/%Y %H:%M', salida) AS salidas FROM registro WHERE consecutivo = ?"""
        values=(f"{consecutivo}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        configuracion=get_configuration()
        
        if configuracion != None:
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
            enviar_correo=False if configuracion[0][20] == 0 else True
            settings.preview_cash=configuracion[0][21]
            vista_previa_cuadre=False if configuracion[0][21] == 0 else True
            settings.print_cash_receipt=configuracion[0][22]
            imprimir_cuadre=False if configuracion[0][22] == 0 else True
            settings.printer=configuracion[0][23]
            impresora=configuracion[0][23]
            settings.paper_width=configuracion[0][24]
            papel=configuracion[0][24]

        placa=registros[0][2]
        entrada=registros[0][3]
        salida=registros[0][4]
        vehiculo=registros[0][5]
        valor=registros[0][7]
        tiempo=registros[0][8]
        vlr_total=registros[0][9]
        correo_electronico=registros[0][13]
        entradas=registros[0][14]
        salidas=registros[0][15]

        consecutivo=settings.consecutivo2
        settings.correo_electronico=correo_electronico

        comentario1="Sin éste recibo no se entrega el automotor."
        comentario2="Después de retirado el automotor no se"
        comentario3="aceptan reclamos."

        if vlr_total == 0:
            showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placa, entrada, comentario1, comentario2, comentario3, entradas)
        if vlr_total > 0:
            showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placa, entrada, salida, valor, tiempo, vlr_total, entradas, salidas)
    except Exception as e:
        print(e)

def showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    settings.consecutivo2=consecutivo
    consecutivo=str(consecutivo).zfill(7) if str(consecutivo[0:1]) == str(settings.prefijo[0:1]) else str(consecutivo)
    consecutivo="Recibo " + consecutivo
    entrada=str(entrada)
    entrada=str(entrada[0:19])
    entrada=f"Entrada " + str(entradas)

    # pdf=FPDF("P", "mm", (int(str(settings.paper_width)[0:2]), 150))
    pdf=FPDF("P", "mm", (settings.paper_width, 150))
    pdf.add_page()
    # pdf.image("assets/img/parqueadero.png", x=0, y=0, w=20, h=20)
    pdf.set_font("helvetica", "", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
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
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    consecutivo_w=pdf.get_string_width(consecutivo)
    pdf.set_x((doc_w - consecutivo_w) / 2)
    pdf.cell(consecutivo_w, 107, consecutivo, align="C")
    placas1=f"Placa {placas}"
    placas1_w=pdf.get_string_width(placas1)
    pdf.set_x((doc_w - placas1_w) / 2)
    pdf.cell(placas1_w, 125, placas1, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
    entrada_w=pdf.get_string_width(entrada)
    pdf.set_x((doc_w - entrada_w) / 2)
    pdf.cell(entrada_w, 142, entrada, align="C")
    pdf.set_font("helvetica", "", size=10 if settings.paper_width == 80 else 8)
    comentario1_w=pdf.get_string_width(comentario1)
    pdf.set_x((doc_w - comentario1_w) / 2)
    pdf.cell(comentario1_w, 157, comentario1, align="C")
    comentario2_w=pdf.get_string_width(comentario2)
    pdf.set_x((doc_w - comentario2_w) / 2)
    pdf.cell(comentario2_w, 164, comentario2, align="C")
    comentario3_w=pdf.get_string_width(comentario3)
    pdf.set_x((doc_w - comentario3_w) / 2)
    pdf.cell(comentario3_w, 171, comentario3, align="C")
    pdf.set_font("helvetica", "", size=15)
    # img=qrcode.make(f"{placas}")
    # pdf.image(img.get_image(), x=25 if int(str(settings.paper_width)[0:2]) == 80 else 14, y=98, w=30, h=30)
    pdf.set_font("helvetica", "", size=15)
    # pdf.code39(f"*{placas}*", x=0, y=70, w=4, h=20)
    if vehiculo == "Moto":
        # pdf.code39(f"*{placas}*", x=2, y=130, w=2, h=15)
        pdf.code39(f"*{placas}*", x=2, y=100, w=2, h=15)
    if vehiculo == "Carro":
        pdf.code39(f"*{placas}*", x=2, y=100, w=2, h=15)
    if vehiculo == "Otro":
        pdf.code39(f"*{placas}*", x=2, y=100, w=2, h=15)
    pdf.set_font("helvetica", "", size=8)
    impreso="                        Software Propio\nImpreso por Gabriel J Hoyos G NIT 98573207" if settings.billing == 1 else ""
    impreso_w=pdf.get_string_width(impreso)
    pdf.set_x((doc_w - impreso_w) / 2)
    pdf.set_y(120)
    pdf.write(0, impreso)
    pdf.output(path+"receipt.pdf")

    if settings.tipo_app == 0:
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

    if settings.send_email_register == 1:
        settings.progressBar.visible=True
        settings.page.open(dlg_modal2)
        settings.page.update()

        bgcolor="blue"
        message="Enviando correo"
        settings.message=message
        settings.showMessage(bgcolor)

        send_mail_billing(config("EMAIL_USER"), settings.correo_electronico)

        bgcolor="green"
        message="Correo enviado satisfactoriamente"
        settings.message=message
        settings.showMessage(bgcolor)

        settings.progressBar.visible=False
        settings.page.close(dlg_modal2)
        settings.page.update()

def showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placas, entrada, salida, valor, tiempo, vlr_total, entradas, salidas):
    nit="NIT " + nit
    # regimen="Régimen " + regimen
    telefono="Teléfono " + telefono
    servicio= "Servicio " + servicio
    settings.consecutivo2=consecutivo
    # consecutivo=str(settings.consecutivo2).zfill(7) if str(settings.consecutivo2[0:1]) == str(settings.prefijo[0:1]) else str(settings.consecutivo2)
    if settings.billing == 0:
        consecutivo="Recibo " + consecutivo
    else:
        consecutivo=settings.prefijo + str(consecutivo).zfill(7)
        settings.consecutivo2=consecutivo
    formato=f"%Y-%m-%d %H:%M"
    entrada=str(entrada)
    salida=str(salida)
    entrada=str(entrada[0:16])
    salida=str(salida[0:16])
    fecha=str(salida[0:16])
    fecha=fecha.split(" ")
    generacion=fecha[0]
    hora=fecha[1]
    generacion=generacion.split("-")
    generacion=generacion[2] + "/" + generacion[1] + "/" + generacion[0] + " " + hora
    expedicion=generacion
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
        doc_adq=settings.cliente_final
        val_fac=vlr_total
        CodImp1="01"
        ValImp1=0
        CodImp2="04"
        ValImp2=0
        CodImp3="03"
        ValImp3=0
        val_iva=0
        val_otro_im=0
        val_tol_fac=val_fac
        ValTot=val_fac+ValImp1+ValImp2+ValImp3
        NitOFE=nit_fac
        ClTec=settings.clave_tecnica
        TipoAmbie=settings.tipo_ambiente
        cufe=f"{consecutivo}" + f"{fec_fac}" + f"{hor_fac}" + f"{val_fac:.2f}" + f"{CodImp1}" + f"{ValImp1:.2f}" + f"{CodImp2}" + f"{ValImp2:.2f}" + f"{CodImp3}" + f"{ValImp3:.2f}" + f"{ValTot:.2f}" + f"{NitOFE}" + f"{doc_adq}" + f"{ClTec}" + f"{TipoAmbie}"
        bytes=cufe.encode('utf-8')
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
                vlr_total=valor_turno
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
    pdf.set_font("helvetica", "", size=20 if settings.paper_width == 80 else 16)
    title_w=pdf.get_string_width(title)
    doc_w=pdf.w
    pdf.set_x((doc_w - title_w) / 2)
    pdf.cell(title_w, 0, title, align="C")
    pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
    parqueadero_w=pdf.get_string_width(parqueadero)
    pdf.set_x((doc_w - parqueadero_w) / 2)
    pdf.cell(parqueadero_w, 18, parqueadero, align="C")
    pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
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
    if settings.billing == 1:
        pdf.set_font("helvetica", "B", size=15 if settings.paper_width == 80 else 11)
        factura="Factura Electrónica de Venta"
        factura_w=pdf.get_string_width(factura)
        pdf.set_x((doc_w - factura_w) / 2)
        pdf.cell(factura_w, 104, factura, align="C")
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        consecutivo1_w=pdf.get_string_width(consecutivo)
        pdf.set_x((doc_w - consecutivo1_w) / 2)
        pdf.cell(consecutivo1_w, 119, consecutivo, align="C")
        pdf.set_font("helvetica", "", size=13 if settings.paper_width == 80 else 10)
        fecha_autoriza1="Desde " + str(fecha_desde) + " Hasta " + str(fecha_hasta)
        fecha_autoriza1_w=pdf.get_string_width(fecha_autoriza1)
        pdf.set_x((doc_w - fecha_autoriza1_w) / 2)
        pdf.cell(fecha_autoriza1_w, 132, fecha_autoriza1, align="C")
        pdf.set_font("helvetica", "", size=13 if settings.paper_width == 80 else 11)
        autoriza1="Autoriza del " + str(autoriza_del) + " al " + str(autoriza_al)
        autoriza1_w=pdf.get_string_width(autoriza1)
        pdf.set_x((doc_w - autoriza1_w) / 2)
        pdf.cell(autoriza1_w, 144, autoriza1, align="C")
        resolucion1="Resolución " + str(resolucion)
        resolucion1_w=pdf.get_string_width(resolucion1)
        pdf.set_x((doc_w - resolucion1_w) / 2)
        pdf.cell(resolucion1_w, 156, resolucion1, align="C")
        forma_pago=f"Forma de Pago Contado"
        forma_pago_w=pdf.get_string_width(forma_pago)
        pdf.set_x((doc_w - forma_pago_w) / 2)
        pdf.cell(forma_pago_w, 170, forma_pago, align="C")
        generacion=f"Fecha Generación " + generacion
        generacion_w=pdf.get_string_width(generacion)
        pdf.set_x((doc_w - generacion_w) / 2)
        pdf.cell(generacion_w, 184, generacion, align="C")
        expedicion=f"Fecha Expedición " + expedicion
        expedicion_w=pdf.get_string_width(expedicion)
        pdf.set_x((doc_w - expedicion_w) / 2)
        pdf.cell(expedicion_w, 198, expedicion, align="C")
        cod_cliente=f"Cliente: {settings.cliente_final}"
        cod_cliente_w=pdf.get_string_width(cod_cliente)
        pdf.set_x((doc_w - cod_cliente_w) / 2)
        pdf.cell(cod_cliente_w, 212, cod_cliente, align="C")
        cliente=f"Consumidor Final"
        cliente_w=pdf.get_string_width(cliente)
        pdf.set_x((doc_w - cliente_w) / 2)
        pdf.cell(cliente_w, 226, cliente, align="C")
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        placas1=f"Placa {placas}"
        placas1_w=pdf.get_string_width(placas1)
        pdf.set_x((doc_w - placas1_w) / 2)
        pdf.cell(placas1_w, 240, placas1, align="C")
        pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
        entrada_w=pdf.get_string_width(entrada)
        pdf.set_x((doc_w - entrada_w) / 2)
        pdf.cell(entrada_w, 254, entrada, align="C")
        salida_w=pdf.get_string_width(salida)
        pdf.set_x((doc_w - salida_w) / 2)
        pdf.cell(salida_w, 268, salida, align="C")
        duracion_w=pdf.get_string_width(duracion)
        pdf.set_x((doc_w - duracion_w) / 2)
        pdf.cell(duracion_w, 282, duracion, align="C")
        tarifa_w=pdf.get_string_width(tarifa)
        pdf.set_x((doc_w - tarifa_w) / 2)
        pdf.cell(tarifa_w, 296, tarifa, align="C")
        valor=locale.currency(valor, grouping=True)
        valor="Valor Unidad " + str(valor) 
        valor_w=pdf.get_string_width(valor)
        pdf.set_x((doc_w - valor_w) / 2)
        pdf.cell(valor_w, 310, valor, align="C")
        vlr_total=locale.currency(vlr_total, grouping=True)
        vlr_total="Total " + str(vlr_total) 
        vlr_total_w=pdf.get_string_width(vlr_total)
        pdf.set_x((doc_w - vlr_total_w) / 2)
        pdf.cell(vlr_total_w, 324, vlr_total, align="C")
        pdf.set_font("helvetica", "", size=13)
        title_cufe="CUFE:"
        title_cufe_w=pdf.get_string_width(title_cufe)
        pdf.set_x((doc_w - title_cufe_w) / 2)
        pdf.cell(title_cufe_w, 338, title_cufe, align="C")
        cufe_w=pdf.get_string_width(cufe)
        pdf.set_x((doc_w - cufe_w) / 2)
        pdf.set_y(184)
        pdf.write(0, cufe)
        img=qrcode.make(f"NumFac: {num_fac}\nFecFac: {fec_fac}\nHorFac: {hor_fac}\nNitFac: {nit_fac}\nDocAdq: {doc_adq}\nValFac: {val_fac:.2f}\nValIva: {val_iva:.2f}\nValOtroim: {val_otro_im:.2f}\nValTolFac: {val_tol_fac:.2f}\nCUFE: {cufe}")
        pdf.image(img.get_image(), x=28 if settings.paper_width == 80 else 14, y=204, w=25, h=25)
    else:
        pdf.set_font("helvetica", "B", size=20 if settings.paper_width == 80 else 16)
        consecutivo_w=pdf.get_string_width(consecutivo)
        pdf.set_x((doc_w - consecutivo_w) / 2)
        pdf.cell(consecutivo_w, 107, consecutivo, align="C")
        placas1=f"Placa {placas}"
        placas1_w=pdf.get_string_width(placas1)
        pdf.set_x((doc_w - placas1_w) / 2)
        pdf.cell(placas1_w, 125, placas1, align="C")
        pdf.set_font("helvetica", "", size=15 if settings.paper_width == 80 else 11)
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
    pdf.set_font("helvetica", "", size=8)
    impreso="                        Software Propio\nImpreso por Gabriel J Hoyos G NIT 98573207" if settings.billing == 1 else ""
    impreso_w=pdf.get_string_width(impreso)
    pdf.set_x((doc_w - impreso_w) / 2)
    if settings.billing == 0:
        pdf.set_y(125)
    else:
        pdf.set_y(231)
    pdf.write(0, impreso)
    pdf.output(path+"receipt.pdf")

    if settings.tipo_app == 0:
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

    if settings.send_email_register == 1:
        settings.progressBar.visible=True
        settings.page.open(dlg_modal2)
        settings.page.update()

        bgcolor="blue"
        message="Enviando correo"
        settings.message=message
        settings.showMessage(bgcolor)

        send_mail_billing(config("EMAIL_USER"), settings.correo_electronico)

        bgcolor="green"
        message="Correo enviado satisfactoriamente"
        settings.message=message
        settings.showMessage(bgcolor)

        settings.progressBar.visible=False
        settings.page.close(dlg_modal2)
        settings.page.update()

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
    sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario = ?"""
    values=(f"{usuario}",)
    cursor.execute(sql, values)
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
                        DataCell(Checkbox(value=False if x["acceso_usuario"] == 0 else True, data=x, on_change=update_access, disabled=True if usuario == "Super Admin" or usuario == "Admin" else False)),
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
    usuario=e.control.data
    title="Eliminar"
    message=f"Desea eliminar el usuario {usuario} ?"
    open_dlg_modal(e, title, message) 

def close_dlg(e):
    dlg_modal.open=False
    settings.page.update()

def open_dlg_modal(e, title, message):
    dlg_modal.title=Text(title, text_align="center")
    dlg_modal.content=Text(message, text_align="center")
    # settings.page.dialog=dlg_modal
    dlg_modal.open=True
    settings.page.overlay.append(dlg_modal)
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
        else:
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
            sql=f"""SELECT usuario, nombre, foto FROM usuarios"""
            cursor.execute(sql)
        else:
            sql="""SELECT usuario, nombre, foto FROM usuarios WHERE usuario LIKE ? OR nombre LIKE ?"""
            values=(f'%{search}%', f'%{search}%')
            cursor.execute(sql, values)
    # elif settings.username["username"] == "Admin":
    elif settings.username == "Admin":
        if search == "":
            sql="""SELECT usuario, nombre, foto FROM usuarios WHERE usuario <> ?"""
            values=(f'{user}',)
        else:
            sql="""SELECT usuario, nombre, foto FROM usuarios WHERE usuario <> ? AND (usuario LIKE ? OR nombre LIKE ?)"""
            values=(f'{user}', f'%{search}%', f'%{search}%')
        cursor.execute(sql, values)
    registros=cursor.fetchall()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["usuario", "nombre", "foto"]
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
                        DataCell(Image(src=f"upload\\img\\" + x["foto"] if settings.tipo_app == 0 else f"img/" + x["foto"], height=50, width=50, fit=ImageFit.COVER, border_radius=150)),
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
                        		on_click=show_delete,
                                visible=False if x["usuario"] == "Super Admin" or x["usuario"] == "Admin" else True
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
    sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario = ?"""
    values=(f'{username}',)
    cursor.execute(sql, values)
    registros=cursor.fetchall()

    if registros != []:
        settings.acceso_usuarios=registros[0][1]
        settings.acceso_configuracion=registros[1][1]
        settings.acceso_variables=registros[2][1]
        settings.acceso_registro=registros[3][1]
        settings.acceso_cuadre=registros[4][1]
        settings.acceso_cierre=registros[5][1]

def selectRegisters(search):
    cuadre=0
    cursor=conn.cursor()
    # sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, tiempo, total, cuadre, usuario FROM registro"""
    if search == "":
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), total, correo_electronico FROM registro WHERE cuadre = ?"""
        values=(f'{cuadre}',)
    else:
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), total, correo_electronico FROM registro WHERE (consecutivo LIKE ? OR placa LIKE ?) AND cuadre = ?"""
        values=(f'%{search}%', f'%{search}%', f'{cuadre}')
    cursor.execute(sql, values)
    registros=cursor.fetchall()

    tb.rows.clear()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["consecutivo", "placa", "entrada", "salida", "total"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            color=colors.GREEN_700 if x["total"] != 0 else None
            weight="bold" if x["total"] != 0 else None
            if settings.billing == 1:
                if x["total"] != 0:
                    settings.consecutivo=settings.prefijo + str(x["consecutivo"]).zfill(7)
                else:
                    settings.consecutivo=str(x["consecutivo"])
            else:
                settings.consecutivo=x["consecutivo"]
            
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
                        # DataCell(Text(x["total"], color=color, weight=weight)),
                        # DataCell(Text(x["cuadre"])),
                        # DataCell(Text(x["usuario"])),
                        # DataCell(Row([
                        # 	# IconButton(icon="create",icon_color="blue",
                        # 	# 	data=x,
                        # 	# 	on_click=showedit
                        # 	# 	),
                        # 	# IconButton(icon="delete",icon_color="red",
                        # 	# 	data=x["id"],
                        # 	# 	on_click=showdelete
                        # 	# 	),
                        #     # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        # 	# 	data=x,
                        # 	# 	on_click=showedit
                        # 	# 	),
                        # ])),
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
        if settings.billing == 1:
            sql=f"""SELECT ? || SUBSTR('0' || consecutivo, -10, 10), placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE cuadre = ?"""
            values=(f'{settings.prefijo}', f'{cuadre}',)
        else:
            sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE cuadre = ?"""
            values=(f'{cuadre}',)
    else:
        if settings.billing == 1:
            sql=f"""SELECT ? || SUBSTR('0' || consecutivo, -10, 10), placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE strftime('%d/%m/%Y', salida) BETWEEN ? AND ? AND cuadre = ?"""
            values=(f'{settings.prefijo}', f'{fecha_desde}', f'{fecha_hasta}', f'{cuadre}')
        else:
            sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), vehiculo, valor, tiempo, total FROM registro WHERE strftime('%d/%m/%Y', salida) BETWEEN ? AND ? AND cuadre = ?"""
            values=(f'{fecha_desde}', f'{fecha_hasta}', f'{cuadre}')
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    return registros

def selectCashRegister():
    cuadre=0
    cursor=conn.cursor()    
    # sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = 0 AND cuadre = 0"""
    sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE cuadre = ?"""
    values=(f'{cuadre}',)
    cursor.execute(sql, values)
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
                        # DataCell(Row([
                        # 	# IconButton(icon="create",icon_color="blue",
                        # 	# 	data=x,
                        # 	# 	on_click=showedit
                        # 	# 	),
                        # 	# IconButton(icon="delete",icon_color="red",
                        # 	# 	data=x["id"],
                        # 	# 	on_click=showdelete
                        # 	# 	),
                        #     # IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        # 	# 	data=x,
                        # 	# 	on_click=showedit
                        # 	# 	),
                        # ])),
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
], height=350)

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

dlg_modal2=AlertDialog(
    modal=True,
    bgcolor=colors.TRANSPARENT,
    content=Column(
        [ProgressRing(),],
        height=15,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    ),
)