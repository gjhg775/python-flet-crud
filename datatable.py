import bcrypt
import datetime
import sqlite3
import hashlib
from flet import *

conn = sqlite3.connect('database/parqueadero.db',check_same_thread=False)

valor=0

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

def get_configuration():
    try:
        id=1
        cursor=conn.cursor()
        sql=f"""SELECT * FROM configuracion WHERE configuracion_id = ?"""
        values=(id,)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros != []:
            parqueadero=registros[0][1]
            nit=registros[0][2]
            regimen=registros[0][3]
            direccion=registros[0][4]
            telefono=registros[0][5]
            servicio=registros[0][6]
            consecutivo=registros[0][7]
            return parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, 
    except Exception as e:
        print(e)

configuracion = get_configuration()

if configuracion != None:
    consecutivo=configuracion[6]

def get_variables():
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM variables"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        if registros != []:
            return registros
    except Exception as e:
        print(e)

variables = get_variables()

if variables != None:
    valor_hora_moto=variables[0][1]
    valor_dia_moto=variables[0][2]
    valor_hora_carro=variables[0][3]
    valor_dia_carro=variables[0][4]
    valor_hora_otro=variables[0][5]
    valor_dia_otro=variables[0][6]

def update_variables(vlr_hora_moto, vlr_dia_moto, vlr_hora_carro, vlr_dia_carro, vlr_hora_otro, vlr_dia_otro, id):
    try:
        cursor=conn.cursor()

        sql=f"""UPDATE variables SET vlr_hora_moto = ?, vlr_dia_moto = ?, vlr_hora_carro = ?, vlr_dia_carro = ?, vlr_hora_otro = ?, vlr_dia_otro = ? WHERE variable_id = ?"""
        values=(f"{vlr_hora_moto}", f"{vlr_dia_moto}", f"{vlr_hora_carro}", f"{vlr_dia_carro}", f"{vlr_hora_otro}", f"{vlr_dia_otro}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def update_register(vehiculo, consecutivo, id):
    try:
        salida=datetime.datetime.now()

        cursor=conn.cursor()

        sql=f"""UPDATE registro SET salida = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE registro_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        id=registros[0][0]
        valor=registros[0][6]
        tiempo=((registros[0][8])/60)/60

        if tiempo <= 4:
            if int(tiempo) == 0:
                total=valor
            else:
                valor_horas=valor*int(tiempo)
                if (((registros[0][9])/60) % 60) == 0:
                    valor_fraccion=0
                if ((registros[0][9])/60) % 60 > 0 and ((registros[0][9])/60) % 60 <= 15:
                    valor_fraccion=valor/2
                if (((registros[0][9])/60) % 60 > 15 and ((registros[0][9])/60) % 60 <= 30) or ((registros[0][9])/60) % 60 > 30:
                    valor_fraccion=valor
                total=valor_horas+valor_fraccion
            if vehiculo == "Moto":
                if total > valor_dia_moto:
                    total=valor_dia_moto
            if vehiculo == "Carro":
                if total > valor_dia_carro:
                    total=valor_dia_carro
            if vehiculo == "Otro":
                total=valor_dia_otro
        else:
            if vehiculo == "Moto":
                total=valor_dia_moto
            if vehiculo == "Carro":
                total=valor_dia_carro
            if vehiculo == "Otro":
                total=valor_dia_otro
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
                        total=total+valor_fraccion+(valor_dia_moto*turno)
                    else:
                        total=valor_dia_moto*turno
                if vehiculo == "Carro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*valor_hora_carro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(valor_dia_carro*turno)
                    else:
                        total=valor_dia_carro*turno
                if vehiculo == "Otro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*valor_hora_otro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(valor_dia_otro*turno)
                    else:
                        total=valor_dia_otro*turno

        tiempo=int(tiempo)
        sql=f"""UPDATE registro SET salida = ?, tiempo = ?, total = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{tiempo}", f"{total}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        id=1
        consecutivo=consecutivo+1
        sql=f"""UPDATE configuracion SET consecutivo = ? WHERE configuracion_id = ?"""
        values=(f"{consecutivo}", f"{id}")
        cursor.execute(sql, values)
        conn.commit()

        return total
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

    tiempo=0
    total=0
    cuadre=0
    usuario="Gabriel Jaime Hoyos Garcés"

    try:
        cursor=conn.cursor()

        id=1
        sql=f"""SELECT consecutivo FROM configuracion WHERE configuracion_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        consecutivo=registros[0][0]

        sql=f"""INSERT INTO registro (consecutivo, placa, entrada, salida, vehiculo, valor, tiempo, total, cuadre, usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{consecutivo}", f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{valor}", f"{tiempo}", f"{total}", f"{cuadre}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def selectRegister(vehiculo, placa):
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida) AND total = 0"""
        values=(f"{placa}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros == []:
            add_register(vehiculo, placa)
            total=0
        else:
            id=registros[0][0]
            consecutivo=registros[0][1]
            total=update_register(vehiculo, consecutivo, id)
        return total

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
    print(f"{e.control.data}")

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

def selectRegisters():
    cursor=conn.cursor()
    # sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, tiempo, total, cuadre, usuario FROM registro"""
    sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida) FROM registro"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != "":
        # keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "tiempo", "total", "cuadre", "usuario"]
        keys=["consecutivo", "placa", "entrada", "salida"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tb.rows.append(
                DataRow(
                    selected=False,
                    data=x["consecutivo"],
                    # data=x,
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

tblRegistro = Column([
    Row([tb], scroll="always")
], height=296)
