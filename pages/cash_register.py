import time
import locale
import flet as ft
import settings
import sqlite3
from pages.receipt import show_cash_register, show_cash_register2
from datatable import tblCuadre, tbc, get_configuration, get_variables, selectCashRegister

conn=sqlite3.connect("C:/pdb/database/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

def Cash_register(page):
    page.window.width=page.width

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
        resolucion=configuracion[0][8]
        fecha_desde=configuracion[0][9]
        fecha_hasta=configuracion[0][10]
        settings.prefijo=configuracion[0][11]
        prefijo=configuracion[0][11]
        autoriza_del=configuracion[0][12]
        autoriza_al=configuracion[0][13]
        clave_tecnica=configuracion[0][14]
        settings.tipo_ambiente=configuracion[0][15]
        tipo_ambiente=configuracion[0][15]
        settings.cliente_final=configuracion[0][16]
        cliente=configuracion[0][16]
        consecutivo=configuracion[0][17]
        settings.preview_register=configuracion[0][18]
        vista_previa_registro=False if configuracion[0][18] == 0 else True
        settings.print_register_receipt=configuracion[0][19]
        imprimir_registro=False if configuracion[0][19] == 0 else True
        settings.preview_cash=configuracion[0][20]
        vista_previa_cuadre=False if configuracion[0][20] == 0 else True
        settings.print_cash_receipt=configuracion[0][21]
        imprimir_cuadre=False if configuracion[0][21] == 0 else True
        settings.printer=configuracion[0][22]
        impresora=configuracion[0][22]
        settings.paper_width=configuracion[0][23]
        papel=configuracion[0][23]

    def cash_register(e):
        total=0
        cuadre=0
        cursor=conn.cursor()
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total > {total} AND cuadre = {cuadre}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        sw=0

        if registros != []:
            show_cash_register(parqueadero, nit, regimen, direccion, telefono, servicio, registros)
            sw=1

        time.sleep(0.1)
        
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = {total} AND cuadre = {cuadre}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        if registros != []:
            show_cash_register2(parqueadero, nit, regimen, direccion, telefono, servicio, registros)
            sw=1

        if sw == 1:
            bgcolor="green"
            message="Cuadre de caja realizado satisfactoriamente"
            settings.message=message
            settings.showMessage(bgcolor)

    btn_cuadre=ft.ElevatedButton(text="Hacer cuadre", icon=ft.icons.APP_REGISTRATION, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=cash_register)

    registros=selectCashRegister()
    if registros != []:
        tblCuadre.height=344
    
    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                            ft.Text("Cuadre de caja", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
                            # ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
                            # ft.ElevatedButton("Registro", on_click=showInputs)
                        ])
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(
                # bgcolor=ft.colors.PRIMARY_CONTAINER,
                # border_radius=10,
                alignment=ft.alignment.center,
                # padding=ft.padding.only(10, 20, 10, 0),
                padding=ft.padding.only(10, 25, 10, 0),
                content=ft.Stack([
                # content=ft.ResponsiveRow([
                        ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
                        ft.Column(col={"xs":12, "sm":12, "md":12, "lg":12, "xl":10, "xxl":8}, controls=[tblCuadre]),
                        ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
                    # ]),
                ]),
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    btn_cuadre
                ]),
            ),
        ]
    )