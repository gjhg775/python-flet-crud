import datetime
import sqlite3
from flet import *

conn = sqlite3.connect('database/parqueadero.db',check_same_thread=False)

valor=0

tb = DataTable(
    bgcolor="#FFFFFF",
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

def get_configuration():
    try:
        id=1
        cursor=conn.cursor()
        sql=f"""SELECT * FROM configuracion WHERE configuracion_id = {id}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        if registros != []:
            parqueadero=registros[0][1]
            regimen=registros[0][3]
            return parqueadero, regimen
    except Exception as e:
        print(e)

configuracion = get_configuration()

if configuracion != None:
    consecutivo=configuracion[0][7]

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
    vlr_hora_moto=variables[0][0]
    vlr_dia_moto=variables[0][1]
    vlr_hora_carro=variables[0][2]
    vlr_dia_carro=variables[0][3]
    vlr_hora_otro=variables[0][4]
    vlr_dia_otro=variables[0][5]

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
                if total > vlr_dia_moto:
                    total=vlr_dia_moto
            if vehiculo == "Carro":
                if total > vlr_dia_carro:
                    total=vlr_dia_carro
            if vehiculo == "Otro":
                total=vlr_dia_otro
        else:
            if vehiculo == "Moto":
                total=vlr_dia_moto
            if vehiculo == "Carro":
                total=vlr_dia_carro
            if vehiculo == "Otro":
                total=vlr_dia_otro
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
                        total=int(round(horas))*vlr_hora_moto
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(vlr_dia_moto*turno)
                    else:
                        total=vlr_dia_moto*turno
                if vehiculo == "Carro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*vlr_hora_carro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(vlr_dia_carro*turno)
                    else:
                        total=vlr_dia_carro*turno
                if vehiculo == "Otro":
                    if int(round(horas)) <= 4:
                        total=int(round(horas))*vlr_hora_otro
                        if ((int(round(horas))/60) % 60) == 0:
                            valor_fraccion=0
                        if ((int(round(horas))/60) % 60) > 0 and ((int(round(horas))/60) % 60) <= 15:
                            valor_fraccion=valor/2
                        if (((int(round(horas))/60) % 60) > 15 and ((int(round(horas))/60) % 60) <= 30) or ((int(round(horas))/60) % 60) > 30:
                            valor_fraccion=valor
                        total=total+valor_fraccion+(vlr_dia_otro*turno)
                    else:
                        total=vlr_dia_otro*turno

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
        valor=vlr_hora_moto
    if vehiculo == "Carro":
        valor=vlr_hora_carro
    if vehiculo == "Otro":
        valor=vlr_hora_otro

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