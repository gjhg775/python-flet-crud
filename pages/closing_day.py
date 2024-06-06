import locale
import flet as ft
import sqlite3
from pages.receipt import show_cash_register
from datatable import tblCuadre, tbc, get_configuration, get_variables, selectRegisters, selectRegister

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

def Closing_day(page):
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
    
    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                            ft.Text("Cierre de día", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
                            # ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
                            # ft.ElevatedButton("Registro", on_click=showInputs)
                        ])
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    # ft.ElevatedButton("Inicio", on_click=lambda _:page.go("/"), icon=ft.icons.HOME),
                    # ft.Row([
                    #     tblRegistro,
                    #     card
                    # ]),
                    # ft.ResponsiveRow([
                    #     ft.Column(col=6, controls=[tblRegistro]),
                    #     ft.Column(col=6, controls=[rdbVehiculo, placa, total])
                    # ]),
                ]),
            ),
            # ft.Container(height=50),
            ft.Container(
                # bgcolor=ft.colors.PRIMARY_CONTAINER,
                # border_radius=10,
                alignment=ft.alignment.center,
                padding=ft.padding.only(10, 20, 10, 0),
                # content=ft.Stack([
                # content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                #         ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[buscar, tblRegistro, no_registros]),
                #         ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[rdbVehiculo, placa]),
                #         ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                #     ]),
                # ]),
            ),
            # ft.Container(
            #     content=ft.ResponsiveRow([
            #         total
            #     ],
            #     alignment=ft.MainAxisAlignment.END
            #     ),
            # ),
        ]
        # ft.Container(
        #     ft.Column([
        #         ft.Container(
        #             alignment=ft.alignment.center,
        #             content=ft.Stack([
        #                 ft.Image(
        #                     src=f"img/fondo.jpg",
        #                     # width=300,
        #                     # height=300,
        #                     fit=ft.ImageFit.COVER
        #                 ),
        #                 ft.Row([
        #                     ft.Column([
        #                         ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
        #                         # ft.ElevatedButton("Registro", on_click=showInputs)
        #                         ft.ElevatedButton("Registro")
        #                     ])
        #                 ], 
        #                 alignment=ft.MainAxisAlignment.CENTER
        #                 ),
        #                 # ft.Row([
        #                     # ft.ElevatedButton("Registro", on_click=showInputs),
        #                     # tblRegistro
        #                     # card
        #                 # ]),
        #                 # card
        #             ]),
        #         )
        #     ])
        # )
    )