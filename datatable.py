import os
import sys
import time
import flet as ft
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
# from flet import *
import flet as ft
from fpdf import FPDF
from pathlib import Path
from decouple import config
from mail import send_mail_billing

# try:
#     conn=sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
# except Exception as e:
#     print(e)

# if settings.tipo_app == 0:
#     conn=sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
# else:
#     conn=sqlite3.connect('C:\\pdb\\data\\parqueadero.db', check_same_thread=False)

def get_connection():
    try:
        return sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
    except Exception as e:
        print(e)

valor=0

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

tbu = ft.DataTable(
    bgcolor=ft.colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
        ft.DataColumn(ft.Text("Foto")),
		ft.DataColumn(ft.Text("Usuario")),
        ft.DataColumn(ft.Text("Correo electrónico")),
		ft.DataColumn(ft.Text("Nombre")),
		ft.DataColumn(ft.Text("Acción")),
	],
	rows=[]
)

tba = ft.DataTable(
    bgcolor=ft.colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		ft.DataColumn(ft.Text("Programa")),
		ft.DataColumn(ft.Text("Acceso")),
		# DataColumn(Text("Acción")),
	],
	rows=[]
)

tb = ft.DataTable(
    bgcolor=ft.colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
    sort_column_index=0,
    sort_ascending=True,
	columns=[
		ft.DataColumn(ft.Text("Consecutivo"), on_sort=lambda e: sort_registers(e)),
		ft.DataColumn(ft.Text("Placa"), on_sort=lambda e: sort_registers(e)),
		ft.DataColumn(ft.Text("Entrada"), on_sort=lambda e: sort_registers(e)),
		ft.DataColumn(ft.Text("Salida"), on_sort=lambda e: sort_registers(e)),
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

tbc = ft.DataTable(
    bgcolor=ft.colors.PRIMARY_CONTAINER,
    # bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
    sort_column_index=0,
    sort_ascending=True,
	columns=[
		ft.DataColumn(ft.Text("Consecutivo"), on_sort=lambda e: sort_cash_register(e)),
		ft.DataColumn(ft.Text("Placa"), on_sort=lambda e: sort_cash_register(e)),
		ft.DataColumn(ft.Text("Entrada"), on_sort=lambda e: sort_cash_register(e)),
		ft.DataColumn(ft.Text("Salida"), on_sort=lambda e: sort_cash_register(e)),
        ft.DataColumn(ft.Text("Vehículo"), on_sort=lambda e: sort_cash_register(e)),
        ft.DataColumn(ft.Text("Facturación"), on_sort=lambda e: sort_cash_register(e)),
        ft.DataColumn(ft.Text("Valor"), numeric=True, on_sort=lambda e: sort_cash_register(e)),
        ft.DataColumn(ft.Text("Tiempo"), numeric=True, on_sort=lambda e: sort_cash_register(e)),
        ft.DataColumn(ft.Text("Total"), numeric=True, on_sort=lambda e: sort_cash_register(e)),
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

id_edit=ft.Text()
vehiculo_edit=ft.RadioGroup(content=ft.Row([
    ft.Radio(label="Moto", value="Moto"),
    ft.Radio(label="Moto", value="Moto"),
    ft.Radio(label="Otro", value="Otro")
]))

def reset_password(usuario):
    try:
        conn=get_connection()
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
        conn.close()

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
        conn=get_connection()
        cursor=conn.cursor()
        sql="""SELECT * FROM usuarios WHERE usuario = ? OR correo_electronico = ?"""
        values=(f'{usuario}', f'{usuario}')
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

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
        conn=get_connection()
        cursor=conn.cursor()
        sql="""SELECT * FROM usuarios WHERE usuario = ? OR correo_electronico = ?"""
        values=(f'{usuario}', f'{usuario}')
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        if registros != []:
            bln_login=False
            return bln_login

        conn=get_connection()
        cursor=conn.cursor()
        sql="""INSERT INTO usuarios (usuario, correo_electronico, clave, nombre, foto) VALUES (?, ?, ?, ?, ?)"""
        values=(f"{usuario}", f"{correo_electronico}", f"{hashed}", f"{nombre}", f"{foto}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        conn=get_connection()
        cursor=conn.cursor()
        user="Admin"
        sql="""SELECT * FROM accesos WHERE usuario = ?"""
        values=(f'{user}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        for registro in registros:
            acceso_usuario=0
            programa=registro[2]
            if programa == "Registro":
                acceso_usuario=1
            conn=get_connection()
            cursor=conn.cursor()
            sql="""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES (?, ?, ?)"""
            values=(f"{usuario}", f"{programa}", f"{acceso_usuario}")
            cursor.execute(sql, values)
            conn.commit()
            conn.close()
    except Exception as e:
        print(e)

def update_user(usuario, correo_electronico, clave, foto, btn):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        if btn == "save":
            hash=hashlib.sha256(clave.encode()).hexdigest()
            sql="""UPDATE usuarios SET clave = ?, foto = ? WHERE usuario = ? OR correo_electronico = ?"""
            values=(f"{hash}", f"{foto}", f"{usuario}", f"{usuario}")
        elif btn == "update":
            sql="""UPDATE usuarios SET correo_electronico = ? WHERE usuario = ?"""
            values=(f"{correo_electronico}", f"{usuario}")
        else:
            sql="""UPDATE usuarios SET foto = ? WHERE usuario = ? OR correo_electronico = ?"""
            values=(f"{foto}", f"{usuario}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        bgcolor="green"
        if btn != "update":
            settings.message="Perfíl actualizado satisfactoriamente"
        else:
            settings.message="Correo electrónico actualizado satisfactoriamente"
        settings.showMessage(bgcolor)
    except Exception as e:
        print(e)

def get_user(usuario):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        if registros != []:
            settings.correo_electronico=registros[0][2]
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
        conn=get_connection()
        cursor=conn.cursor()
        sql="SELECT * FROM configuracion"
        cursor.execute(sql)
        configuracion=cursor.fetchall()
        conn.close()

        if configuracion != []:
            return configuracion
    except Exception as e:
        print(e)

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
    secret_key=configuracion[0][23]
    settings.preview_cash=configuracion[0][24]
    vista_previa_cuadre=False if configuracion[0][24] == 0 else True
    settings.print_cash_receipt=configuracion[0][25]
    imprimir_cuadre=False if configuracion[0][25] == 0 else True
    settings.printer=configuracion[0][26]
    impresora=configuracion[0][26]
    settings.paper_width=configuracion[0][27]
    papel=configuracion[0][27]

def update_configuration(parqueadero, nit, regimen, direccion, telefono, servicio, facturacion, resolucion, fecha_desde, fecha_hasta, prefijo, autoriza_del, autoriza_al, clave_tecnica, tipo_ambiente, cliente, consecutivo, vista_previa_registro, imprimir_registro, enviar_correo_electronico, correo_usuario, correo_clave, secret_key, vista_previa_cuadre, imprimir_cuadre, impresora, papel, id):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""UPDATE configuracion SET parqueadero = ?, nit = ?, regimen = ?, direccion = ?, telefono = ?, servicio = ?, facturacion = ?, resolucion = ?, fecha_desde = ?, fecha_hasta = ?, prefijo = ?, autoriza_del = ?, autoriza_al = ?, clave_tecnica = ?, tipo_ambiente = ?, cliente = ?, consecutivo = ?, vista_previa_registro = ?, imprimir_registro = ?, enviar_correo_electronico = ?, email_user = ?, email_pass = ?, secret_key = ?, vista_previa_cuadre = ?, imprimir_cuadre = ?, impresora = ?, papel = ? WHERE configuracion_id = ?"""
        values=(f"{parqueadero}", f"{nit}", f"{regimen}", f"{direccion}", f"{telefono}", f"{servicio}", f"{facturacion}", f"{resolucion}", f"{fecha_desde}", f"{fecha_hasta}", f"{prefijo}", f"{autoriza_del}", f"{autoriza_al}", f"{clave_tecnica}", f"{tipo_ambiente}", f"{cliente}", f"{consecutivo}", f"{vista_previa_registro}", f"{imprimir_registro}", f"{enviar_correo_electronico}", f"{correo_usuario}", f"{correo_clave}", f"{secret_key}", f"{vista_previa_cuadre}", f"{imprimir_cuadre}", f"{impresora}", f"{papel}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        # settings.billing=facturacion
        # settings.cliente_final=cliente
        # settings.printer=impresora
        # settings.paper_width=papel

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
    except Exception as e:
        print(e)

def get_variables():
    try:
        conn=get_connection()
        cursor=conn.cursor()
        sql="SELECT * FROM variables"
        cursor.execute(sql)
        variables=cursor.fetchall()
        conn.close()

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
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""UPDATE variables SET vlr_hora_moto = ?, vlr_turno_moto = ?, vlr_hora_carro = ?, vlr_turno_carro = ?, vlr_hora_otro = ?, vlr_turno_otro = ? WHERE variable_id = ?"""
        values=(f"{vlr_hora_moto}", f"{vlr_turno_moto}", f"{vlr_hora_carro}", f"{vlr_turno_carro}", f"{vlr_hora_otro}", f"{vlr_turno_otro}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        message="Variables actualizadas satisfactoriamente"
        return message
    except Exception as e:
        print(e)

def update_register_mail(correo_electronico, placa, consecutivo):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""UPDATE registro SET correo_electronico = ? WHERE placa = ? AND consecutivo = ?"""
        values=(f"{correo_electronico}", f"{placa}", f"{consecutivo}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

def update_register(vehiculo, consecutivo, id, valor_hora_moto, valor_turno_moto, valor_hora_carro, valor_turno_carro, valor_hora_otro, valor_turno_otro):
    # usuario=settings.username["username"]
    usuario=settings.username
    
    try:
        salida=datetime.datetime.now()
        formato=f"%Y-%m-%d %H:%M:%S"
        salida=str(salida)
        salida=str(salida[0:19])
        salida=datetime.datetime.strptime(salida, formato)

        if vehiculo == "Moto":
            valor=valor_hora_moto
        if vehiculo == "Carro":
            valor=valor_hora_carro
        if vehiculo == "Otro":
            valor=valor_hora_otro

        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""SELECT entrada AS ent, datetime() AS sal FROM registro WHERE registro_id = ?"""
        values=(f"{id}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

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
            conn=get_connection()
            cursor=conn.cursor()
            sql="""SELECT * FROM usuarios WHERE usuario = ?"""
            values=(f'{usuario}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()
            conn.close()

            usuario=registros[0][4]

            conn=get_connection()
            cursor=conn.cursor()
            sql=f"""UPDATE registro SET salida = ?, valor = ?, retiro = ? WHERE registro_id = ?"""
            values=(f"{salida}", f"{valor}", f"{usuario}", f"{id}")
            cursor.execute(sql, values)
            conn.commit()
            conn.close()

            conn=get_connection()
            cursor=conn.cursor()
            sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE registro_id = ?"""
            values=(f'{id}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()
            conn.close()

            id=registros[0][0]
            placa=registros[0][2]
            entrada=registros[0][3]
            salida=registros[0][4]
            valor=registros[0][7]
            # tiempo=((registros[0][13])/60)/60
            tiempo=registros[0][8]

            formato=f"%Y-%m-%d %H:%M:%S"
            entrada=str(entrada)
            salida=str(salida)
            entrada=str(entrada[0:19])
            salida=str(salida[0:19])
            entrada=datetime.datetime.strptime(entrada, formato)
            salida=datetime.datetime.strptime(salida, formato)
            tiempos=salida - entrada
            dias=tiempos.days*24
            horas=tiempos.seconds//3600
            horas+=dias
            sobrante=tiempos.seconds%3600
            minutos=sobrante//60
            segundos=sobrante//60
            duracion=str(f'{horas:02}') + ":" + str(f'{minutos:02}') + ":" + str(f'{segundos:02}')

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
            tiempo=duracion
            conn=get_connection()
            cursor=conn.cursor()
            sql="""UPDATE registro SET salida = ?, facturacion = ?, valor = ?, tiempo = ?, total = ? WHERE registro_id = ?"""
            values=(f"{salida}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{id}")
            cursor.execute(sql, values)
            conn.commit()
            conn.close()

            conn=get_connection()
            cursor=conn.cursor()
            sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE registro_id = ?"""
            values=(f'{id}',)
            cursor.execute(sql, values)
            registros=cursor.fetchall()
            conn.close()

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
    formato=f"%Y-%m-%d %H:%M:%S"
    entrada=str(entrada)
    entrada=str(entrada[0:19])
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
        conn=get_connection()
        cursor=conn.cursor()
        sql="""SELECT * FROM usuarios WHERE usuario = ?"""
        values=(f'{usuario}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        usuario=registros[0][4]

        conn=get_connection()
        cursor=conn.cursor()
        id=1
        sql="""SELECT consecutivo FROM configuracion WHERE configuracion_id = ?"""
        values=(f'{id}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        consecutivo=registros[0][0]
        correo_electronico=settings.correo_electronico

        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""INSERT INTO registro (consecutivo, placa, entrada, salida, vehiculo, facturacion, valor, tiempo, total, cuadre, ingreso, correo_electronico) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{consecutivo}", f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{facturacion}", f"{valor}", f"{tiempo}", f"{total}", f"{cuadre}", f"{usuario}", f"{correo_electronico}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f'{placa}',)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        correo_electronico=registros[0][13]
        entradas=registros[0][14]
        salidas=registros[0][15]

        conn=get_connection()
        cursor=conn.cursor()
        id=1
        consecutivos=int(consecutivo)+1
        consecutivos=str(consecutivos).zfill(6)
        sql=f"""UPDATE configuracion SET consecutivo = ? WHERE configuracion_id = ?"""
        values=(f"{consecutivos}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        comentario1="Sin éste recibo, no se entrega el automotor."
        comentario2="Después de retirado el automotor, no se"
        comentario3="aceptan reclamos."

        return consecutivo, vehiculo, placa, entrada, salida, tiempo, comentario1, comentario2, comentario3, total, correo_electronico, entradas, salidas
    except Exception as e:
        print(e)

def exist_email(placa):
    settings.correo_electronico=""
    correo_electronico=settings.correo_electronico
    conn=get_connection()
    cursor=conn.cursor()
    sql=f"""SELECT * FROM registro WHERE placa = ? AND correo_electronico != ? ORDER BY salida DESC"""
    values=(f"{placa}", f"{correo_electronico}")
    cursor.execute(sql, values)
    registros=cursor.fetchone()
    conn.close()

    if registros != None:
        settings.correo_electronico=registros[13]

def selectRegister(vehiculo, placa):
    try:
        conn=get_connection()
        cursor=conn.cursor()
        total=0
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = ?"""
        # sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f"{placa}", f"{total}")
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

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
            if total == None or total == "":
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
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""SELECT *, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entradas, strftime('%d/%m/%Y %H:%M:%S', salida) AS salidas FROM registro WHERE consecutivo = ?"""
        values=(f"{consecutivo}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()
        conn.close()

        configuracion=get_configuration()
        
        if configuracion != None:
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

        placa=registros[0][2]
        entrada=registros[0][3]
        salida=registros[0][4]
        vehiculo=registros[0][5]
        valor=registros[0][7]
        tiempo=registros[0][8]
        vlr_total=registros[0][9]
        ingreso=registros[0][11]
        retiro=registros[0][12]
        correo_electronico=registros[0][13]
        entradas=registros[0][14]
        salidas=registros[0][15]

        consecutivo=settings.consecutivo2
        settings.correo_electronico=correo_electronico

        comentario1="Sin éste recibo, no se entrega el automotor."
        comentario2="Después de retirado el automotor, no se"
        comentario3="aceptan reclamos."

        if vlr_total == 0:
            atendido=ingreso
            showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placa, entrada, comentario1, comentario2, comentario3, entradas, atendido)
        if vlr_total > 0:
            atendido=retiro
            showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placa, entrada, salida, valor, tiempo, vlr_total, entradas, salidas)
    except Exception as e:
        print(e)

def showInput(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas, atendido):
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
    placas1=vehiculo + " " + placas1
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
    pdf.set_font("helvetica", "", size=10)
    atendido="Atendido por " + atendido
    atendido_w=pdf.get_string_width(atendido)
    pdf.set_x((doc_w - atendido_w) / 2)
    pdf.cell(atendido_w, 194, atendido, align="C")
    pdf.set_font("helvetica", "", size=15)
    # img=qrcode.make(f"{placas}")
    # pdf.image(img.get_image(), x=25 if int(str(settings.paper_width)[0:2]) == 80 else 14, y=98, w=30, h=30)
    pdf.set_font("helvetica", "", size=15)
    # pdf.code39(f"*{placas}*", x=0, y=70, w=4, h=20)
    if len(placas) == 5:
        pdf.code39(f"*{placas}*", x=12, y=112, w=1.5, h=5)
    elif len(placas) == 6:
        pdf.code39(f"*{placas}*", x=8, y=112, w=1.5, h=5)
    else:
        pdf.code39(f"*{placas}*", x=2, y=112, w=1.2, h=5)
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

    if settings.send_email_register == 1:
        bgcolor="blue"
        message="Enviando correo"
        settings.message=message
        settings.showMessage(bgcolor)

        time.sleep(2)

        settings.progressBar.visible=True
        settings.page.open(dlg_modal2)
        settings.page.update()

        send_mail_billing(settings.email_user, settings.correo_electronico)

        settings.progressBar.visible=False
        settings.page.close(dlg_modal2)
        settings.page.update()

        bgcolor="green"
        message="Correo enviado satisfactoriamente"
        settings.message=message
        settings.showMessage(bgcolor)

        time.sleep(2)

def showOutput(parqueadero, nit, regimen, direccion, telefono, servicio, resolucion, fecha_desde, fecha_hasta, autoriza_del, autoriza_al, consecutivo, vehiculo, placas, entrada, salida, valor, tiempo, vlr_total, entradas, salidas):
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
    entrada=str(entrada[0:19])
    salida=str(salida[0:19])
    fecha=str(salida[0:19])
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

    if dias == 0 and int(horas) <= 3:
        if int(horas) == 0:
            total=valor
        else:
            if vehiculo == "Moto":
                valor_turno=valor_turno_moto
                # tarifa="Tarifa Turno-Moto"
            if vehiculo == "Carro":
                valor_turno=valor_turno_carro
                # tarifa="Tarifa Turno-Carro"
            if vehiculo == "Otro":
                valor_turno=valor_turno_otro
                # tarifa="Tarifa Turno-Otro"

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
        placas1=vehiculo + " " + placas1
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
        placas1=vehiculo + " " + placas1
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
        vlr_total2=vlr_total
        vlr_total2=locale.currency(vlr_total2, grouping=True)
        vlr_total2="Total " + str(vlr_total2) 
        vlr_total2_w=pdf.get_string_width(vlr_total2)
        pdf.set_x((doc_w - vlr_total2_w) / 2)
        pdf.cell(vlr_total2_w, 222, vlr_total2, align="C")
    pdf.set_font("helvetica", "", size=10)
    atendido="Atendido por " + atendido
    atendido_w=pdf.get_string_width(atendido)
    pdf.set_x((doc_w - atendido_w) / 2)
    pdf.cell(atendido_w, 236, atendido, align="C")
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
    settings.usuario=usuario
    if usuario != "Super Admin" and usuario != "Admin":
        programa=acceso["programa"]
        acceso_usuario=0 if chk.value == False else 1
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""UPDATE accesos SET acceso_usuario = ? WHERE programa = ? AND usuario = ?"""
        values=(f"{acceso_usuario}", f"{programa}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

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
    settings.usuario=usuario
    conn=get_connection()
    cursor=conn.cursor()
    sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario = ?"""
    values=(f"{usuario}",)
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["programa", "acceso_usuario"]
        result=[dict(zip(keys, values)) for values in registros]

        tba.rows.clear()

        for x in result:
            tba.rows.append(
                ft.DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=lambda _: None,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        ft.DataCell(ft.Text(x["programa"])),
                        # DataCell(Text(x["acceso_usuario"])),
                        # DataCell(Checkbox(label=x["programa"], value=False if x["acceso_usuario"] == 0 else True)),
                        ft.DataCell(ft.Checkbox(value=False if x["acceso_usuario"] == 0 else True, data=x, on_change=update_access, disabled=True if usuario == "Super Admin" or usuario == "Admin" else False)),
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

# def delete_user(e):
#     usuario=e.control.data["usuario"]
#     show_edit_access(e)
#     show_delete(e)

def show_delete(e):
    usuario=e.control.data["usuario"]
    settings.usuario=usuario
    show_edit_access(e)
    # usuario=settings.usuario
    message=f"Desea eliminar el usuario {usuario} ?"
    open_dlg_modal(e, title, message)

def close_dlg(e):
    dlg_modal.open=False
    dlg_modal.update()

def open_dlg_modal(e, title, message):
    # dlg_modal.title=ft.Text(title, text_align="center")
    dlg_modal.title=ft.Row([
        ft.Icon(ft.icons.DELETE, size=32),
        ft.Text("Eliminar", text_align="center", color=ft.colors.PRIMARY)
    ],
    alignment=ft.MainAxisAlignment.CENTER
    )
    dlg_modal.content=ft.Text(message, text_align="center")
    # settings.page.dialog=dlg_modal
    dlg_modal.open=True
    # settings.page.overlay.append(dlg_modal)
    settings.page.add(dlg_modal)
    settings.page.update()

def user_delete(e):
    usuario=settings.usuario
    usuario2=usuario
    dlg_modal.open=False
    dlg_modal.update()
    try:
        # usuario=e.control.data
        # if usuario == "Super Admin" or usuario == "Admin":
        #     bgcolor="orange"
        #     settings.message=f"El usuario {usuario} no puede ser eliminado"
        #     settings.showMessage(bgcolor)
        # else:

        get_user(usuario)

        if settings.photo != "default.jpg":
            os.remove(os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
        
        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""DELETE FROM accesos WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        conn=get_connection()
        cursor=conn.cursor()
        sql=f"""DELETE FROM usuarios WHERE usuario = ?"""
        values=(f"{usuario}",)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        # tbu.rows.clear()
        # tba.rows.clear()
        search=""
        # selectUsers(search)
        # lblAccesos.value="Accesos"
        # lblAccesos.update()
        # tblUsuarios.update()
        # tblAccesos.update()

        registros=selectUsers(search)
        if registros != []:
            if len(registros) < 4:
                tblUsuarios.height=(len(registros)*50)+50
            else:
                tblUsuarios.height=246
            # no_registros.visible=False
            tblUsuarios.update()
            # usuario=registros[0][0]
            usuario=settings.username
            show_access(usuario)
            # lblAccesos.value="Accesos " + usuario
            # lblAccesos.update()
            # tblAccesos.update()

        usuario=usuario2
        bgcolor="green"
        message=f"Usuario {usuario} eliminado satisfactoriamente"
        settings.message=message
        settings.showMessage(bgcolor)
    except Exception as e:
        print(e)

def selectUsers(search):
    user="Super Admin"
    conn=get_connection()
    cursor=conn.cursor()
    # if settings.username["username"] == "Super Admin":
    if settings.username == "Super Admin":
        if search == "":
            sql=f"""SELECT usuario, correo_electronico, nombre, foto FROM usuarios"""
            cursor.execute(sql)
        else:
            sql="""SELECT usuario, correo_electronico, nombre, foto FROM usuarios WHERE usuario LIKE ?"""
            values=(f"%{search}%",)
            cursor.execute(sql, values)
    # elif settings.username["username"] == "Admin":
    elif settings.username == "Admin":
        if search == "":
            sql="""SELECT usuario, correo_electronico, nombre, foto FROM usuarios WHERE usuario <> ?"""
            values=(f"{user}",)
        else:
            sql="""SELECT usuario, correo_electronico, nombre, foto FROM usuarios WHERE usuario <> ? AND usuario LIKE ?"""
            values=(f"{user}", f"%{search}%")
        cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["usuario", "correo_electronico", "nombre", "foto"]
        result=[dict(zip(keys, values)) for values in registros]

        tbu.rows.clear()

        for x in result:
            tbu.rows.append(
                ft.DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=show_edit_access,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        # ft.DataCell(ft.Image(src=f"{upload_path}\\img\\" + x["foto"] if settings.tipo_app == 0 else f"{upload_path}/img/" + x["foto"], height=50, width=50, fit=ft.ImageFit.COVER, border_radius=150)),
                        ft.DataCell(ft.Image(src=f"/img/" + x["foto"], height=50, width=50, fit=ft.ImageFit.COVER, border_radius=150)),
                        ft.DataCell(ft.Text(x["usuario"])),
                        ft.DataCell(ft.Text(x["correo_electronico"])),
                        ft.DataCell(ft.Text(x["nombre"])),
                        ft.DataCell(ft.Row([
                        	# IconButton(icon="create",icon_color="blue",
                        	# 	data=x,
                        	# 	on_click=showedit
                        	# 	),
                        	ft.IconButton(icon="delete", icon_color=ft.colors.PRIMARY,
                        		# data=x["id"],
                        		data=x,
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

def show_access(usuario):
    user="Super Admin"
    conn=get_connection()
    cursor=conn.cursor()
    if settings.username == user:
        sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario LIKE ?"""
        values=(f"{usuario}",)
    else:
        sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario LIKE ? AND usuario <> ?"""
        values=(f"{usuario}", f"{user}")
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["programa", "acceso_usuario"]
        result=[dict(zip(keys, values)) for values in registros]

        tba.rows.clear()

        for x in result:
            tba.rows.append(
                ft.DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=lambda _: None,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        ft.DataCell(ft.Text(x["programa"])),
                        # DataCell(Text(x["acceso_usuario"])),
                        # DataCell(Checkbox(label=x["programa"], value=False if x["acceso_usuario"] == 0 else True)),
                        ft.DataCell(ft.Checkbox(value=False if x["acceso_usuario"] == 0 else True, disabled=True if usuario == "Super Admin" or usuario == "Admin" else False)),
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
    return registros

def selectAccess(username):
    conn=get_connection()
    cursor=conn.cursor()
    sql="""SELECT programa, acceso_usuario FROM accesos WHERE usuario = ?"""
    values=(f'{username}',)
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    if registros != []:
        settings.acceso_usuarios=registros[0][1]
        settings.acceso_configuracion=registros[1][1]
        settings.acceso_variables=registros[2][1]
        settings.acceso_registro=registros[3][1]
        settings.acceso_cuadre=registros[4][1]
        settings.acceso_cierre=registros[5][1]

def sort_registers(e):
    tb.sort_column_index=e.column_index
    tb.sort_ascending=True if e.ascending else False
    if e.ascending == True:
        order="ASC"
    else:
        order="DESC"
    
    if e.column_index == 0:
        column="consecutivo"
    elif e.column_index == 1:
        column="placa"
    elif e.column_index == 2:
        column="entrada"
    elif e.column_index == 3:
        column="salida"

    order=column + " " + order
    selectRegisters("", order)
    settings.page.update()

def selectRegisters(search="", order="consecutivo ASC"):
    cuadre=0
    conn=get_connection()
    cursor=conn.cursor()
    # sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, tiempo, total, cuadre, usuario FROM registro"""
    if search == "":
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), total, correo_electronico FROM registro WHERE cuadre = ? ORDER BY {order}"""
        values=(f'{cuadre}',)
    else:
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada), strftime('%d/%m/%Y %H:%M:%S', salida), total, correo_electronico FROM registro WHERE (consecutivo LIKE ? OR placa LIKE ?) AND cuadre = ? ORDER BY {order}"""
        values=(f'%{search}%', f'%{search}%', f'{cuadre}')
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    tb.rows.clear()

    if registros != []:
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["consecutivo", "placa", "entrada", "salida", "total"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            color=ft.colors.GREEN_700 if x["total"] != 0 else None
            weight="bold" if x["total"] != 0 else None
            if settings.billing == 1:
                if x["total"] != 0:
                    settings.consecutivo=settings.prefijo + str(x["consecutivo"]).zfill(6)
                else:
                    settings.consecutivo=str(x["consecutivo"])
            else:
                settings.consecutivo=x["consecutivo"]
            
            tb.rows.append(
                ft.DataRow(
                    # color=colors.GREEN_100 if x["total"] != 0 else None,
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=showedit,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        ft.DataCell(ft.Text(x["consecutivo"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["placa"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["entrada"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["salida"], color=color, weight=weight)),
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
    conn=get_connection()
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
    conn.close()
    return registros

def sort_cash_register(e):
    tbc.sort_column_index=e.column_index
    tbc.sort_ascending=True if e.ascending else False
    if e.ascending == True:
        order="ASC"
    else:
        order="DESC"
    
    if e.column_index == 0:
        column="consecutivo"
    elif e.column_index == 1:
        column="placa"
    elif e.column_index == 2:
        column="entrada"
    elif e.column_index == 3:
        column="salida"
    elif e.column_index == 4:
        column="vehiculo"
    elif e.column_index == 5:
        column="facturacion"
    elif e.column_index == 6:
        column="valor"
    elif e.column_index == 7:
        column="tiempo"
    elif e.column_index == 8:
        column="total"

    order=column + " " + order
    selectCashRegister(order)
    settings.page.update()

def selectCashRegister(order="consecutivo ASC"):
    cuadre=0
    conn=get_connection()
    cursor=conn.cursor()    
    # sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = 0 AND cuadre = 0"""
    sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M:%S', entrada) AS entrada, strftime('%d/%m/%Y %H:%M:%S', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE cuadre = ? order by {order}"""
    values=(f'{cuadre}',)
    cursor.execute(sql, values)
    registros=cursor.fetchall()
    conn.close()

    tbc.rows.clear()

    if registros != []:
        keys=["consecutivo", "placa", "entrada", "salida", "vehiculo", "facturacion", "valor", "tiempo", "total", "cuadre"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            color=ft.colors.GREEN_700 if x["total"] != 0 else None
            weight="bold" if x["total"] != 0 else None
            tbc.rows.append(
                ft.DataRow(
                    selected=False,
                    # data=x["id"],
                    data=x,
                    on_select_changed=lambda _: None,
                    # on_select_changed=lambda e: print(f"ID select: {e.control.data}"),
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        ft.DataCell(ft.Text(x["consecutivo"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["placa"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["entrada"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["salida"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["vehiculo"], color=color, weight=weight)),
                        ft.DataCell(ft.Text("Horas" if x["facturacion"] == 0 else "Turnos", color=color, weight=weight)),
                        ft.DataCell(ft.Text(locale.currency(x["valor"], grouping=True), color=color, weight=weight)),
                        ft.DataCell(ft.Text(x["tiempo"], color=color, weight=weight)),
                        ft.DataCell(ft.Text(locale.currency(x["total"], grouping=True), color=color, weight=weight)),
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

lblAccesos=ft.Text("Accesos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)

tblUsuarios = ft.Column([
    ft.Row([tbu], scroll="always")
], height=60, scroll="always")

tblAccesos = ft.Column([
    ft.Row([tba], scroll="always")
], height=350)

tblRegistro = ft.Column([
    ft.Row([tb], scroll="always")
], height=60, scroll="always")

tblCuadre = ft.Column([
    ft.Row([tbc], scroll="always")
], height=60, scroll="always")

dlg_modal=ft.AlertDialog(
    bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
    modal=True,
    # icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
    # title=Text(title, text_align="center"),
    # content=Text(message, text_align="center"),
    actions=[
        ft.TextButton("Sí", on_click=user_delete),
        ft.TextButton("No", autofocus=True, on_click=close_dlg)
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    # on_dismiss=lambda _: date_button.focus(),
)

dlg_modal2=ft.AlertDialog(
    modal=True,
    bgcolor=ft.colors.TRANSPARENT,
    content=ft.Column(
        [ft.ProgressRing(),],
        height=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),
)