from flet import *
import datetime
import sqlite3

conn = sqlite3.connect('database/parqueadero.db',check_same_thread=False)

valor=0

tb = DataTable(
    bgcolor="#FFFFFF",
    # border_radius=10,
    # data_row_color={"hovered": "#e5eff5"},
	columns=[
		DataColumn(Text("ID")),
		DataColumn(Text("Placa")),
		DataColumn(Text("Entrada")),
		DataColumn(Text("Salida")),
        DataColumn(Text("Vehiculo")),
        DataColumn(Text("Valor")),
        DataColumn(Text("Total")),
        # DataColumn(Text("Cuadre")),
        # DataColumn(Text("Usuario")),
		DataColumn(Text("Acción")),
	],
	rows=[]
)

id_edit=Text()
vehiculo_edit=RadioGroup(content=Row([
    Radio(label="Moto", value="Moto"),
    Radio(label="Moto", value="Moto"),
    Radio(label="Otro", value="Otro")
]))

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

def update_register(vehiculo, placa):
    try:
        salida=datetime.datetime.now()

        cursor=conn.cursor()

        sql=f"""UPDATE registro SET salida = ? WHERE placa = ? AND entrada = salida"""
        values=(f"{salida}", f"{placa}")
        cursor.execute(sql, values)
        conn.commit()

        sql=f"""SELECT *, strftime("%s", salida) - strftime("%s", entrada) AS tiempo FROM registro WHERE placa = '{placa}'"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        id=registros[0][0]
        valor=registros[0][5]
        tiempo=((registros[0][9])/60)/60

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

        sql=f"""UPDATE registro SET salida = ?, total = ? WHERE registro_id = ?"""
        values=(f"{salida}", f"{total}", f"{id}")
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

    total=0
    cuadre=0
    usuario="Gabriel Jaime Hoyos Garcés"

    try:
        cursor=conn.cursor()
        sql=f"""INSERT INTO registro (placa, entrada, salida, vehiculo, valor, total, cuadre, usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        values=(f"{placa}", f"{entrada}", f"{salida}", f"{vehiculo}", f"{valor}", f"{total}", f"{cuadre}", f"{usuario}")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def selectRegister(vehiculo, placa):
    try:
        cursor=conn.cursor()
        sql=f"""SELECT * FROM registro WHERE placa = ? AND strftime("%s", entrada) = strftime("%s", salida)"""
        values=(f"{placa}",)
        cursor.execute(sql, values)
        registros=cursor.fetchall()

        if registros == []:
            add_register(vehiculo, placa)
        else:
            total=update_register(vehiculo, placa)
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
    data_edit=e.control.data
    id_edit=data_edit["id"]

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
    sql=f"""SELECT registro_id, placa, strftime('%d/%m/%Y %H:%M', entrada), strftime('%d/%m/%Y %H:%M', salida), vehiculo, valor, total, cuadre, usuario FROM registro"""
    cursor.execute(sql)
    registros=cursor.fetchall()

    if registros != "":
        keys=["id", "placa", "entrada", "salida", "vehiculo", "valor", "total", "cuadre", "usuario"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tb.rows.append(
                DataRow(
                    # selected=False,
                    # on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    cells=[
                        DataCell(Text(x["id"])),
                        DataCell(Text(x["placa"])),
                        DataCell(Text(x["entrada"])),
                        DataCell(Text(x["salida"])),
                        DataCell(Text(x["vehiculo"])),
                        DataCell(Text(x["valor"])),
                        DataCell(Text(x["total"])),
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
                            IconButton(icon="picture_as_pdf_rounded",icon_color="blue",
                        		data=x,
                        		on_click=showedit
                        		),
                        	])),
                    ],
                ),
            )

tblRegistro = Column([
    Row([tb], scroll="always")
], height=296)