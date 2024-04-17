from flet import *
import sqlite3
conn = sqlite3.connect('database/parqueadero.db',check_same_thread=False)

tb = DataTable(
    bgcolor="#FFFFFF",
    border_radius=10,
	columns=[
		DataColumn(Text("ID", size=20)),
		DataColumn(Text("Placa", size=20)),
		DataColumn(Text("Entrada", size=20)),
		DataColumn(Text("Salida", size=20)),
		DataColumn(Text("Acción", size=20)),
	],
	rows=[]
)

def showedit():
    pass

def showdelete():
	pass

def selectRegisters():
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM registro")
    registros=cursor.fetchall()

    if registros != "":
        keys=["id", "placa", "entrada", "salida"]
        result=[dict(zip(keys, values)) for values in registros]

        for x in result:
            tb.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(x["id"])),
                        DataCell(Text(x["placa"])),
                        DataCell(Text(x["entrada"])),
                        DataCell(Text(x["salida"])),
                        DataCell(Row([
                        	IconButton(icon="create",icon_color="blue",
                        		data=x,
                        		on_click=showedit
                        		),
                        	IconButton(icon="delete",icon_color="red",
                        		data=x["id"],
                        		on_click=showdelete
                        		),
                        	])),
                    ],
                ),
            )

tblRegistro = Column([
				Row([tb],scroll="always")
			])