import time
import locale
import flet as ft
import sqlite3
from pages.receipt import show_cash_register, show_cash_register2
from datatable import tblCuadre, tbc, get_configuration, get_variables, selectCashRegister

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

def Cash_register(page):
    page.window_width=page.width

    configuracion=get_configuration()

    if configuracion != None:
        id=configuracion[0][0]
        parqueadero=configuracion[0][1]
        nit=configuracion[0][2]
        regimen=configuracion[0][3]
        direccion=configuracion[0][4]
        telefono=configuracion[0][5]
        servicio=configuracion[0][6]
        # consecutivo=configuracion[0][7]

    def cash_register(e):
        total=0
        cuadre=0
        cursor=conn.cursor()
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total > {total} AND cuadre = {cuadre}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        if registros != []:
            show_cash_register(parqueadero, nit, regimen, direccion, telefono, servicio, registros)

        time.sleep(0.1)
        
        sql=f"""SELECT consecutivo, placa, strftime('%d/%m/%Y %H:%M', entrada) AS entrada, strftime('%d/%m/%Y %H:%M', salida) AS salida, vehiculo, facturacion, valor, tiempo, total, cuadre FROM registro WHERE total = {total} AND cuadre = {cuadre}"""
        cursor.execute(sql)
        registros=cursor.fetchall()

        if registros != []:
            show_cash_register2(parqueadero, nit, regimen, direccion, telefono, servicio, registros)

    # tbc.rows.clear()
    # selectCashRegister()

    no_registros=ft.Text("No se encontraron registros", visible=True)
    btn_cuadre=ft.ElevatedButton(text="Hacer cuadre", icon=ft.icons.APP_REGISTRATION, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=cash_register)

    tbc.rows.clear()
    registros=selectCashRegister()
    if registros != []:
        tblCuadre.height=344
        no_registros.visible=False
    
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
                        ft.Column(col={"xs":12, "sm":12, "md":12, "lg":12, "xl":10, "xxl":8}, controls=[tblCuadre, no_registros]),
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