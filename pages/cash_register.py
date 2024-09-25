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
        settings.send_email_register=configuracion[0][20]
        enviar_correo_electronico=False if configuracion[0][20] == 0 else True
        settings.preview_cash=configuracion[0][21]
        vista_previa_cuadre=False if configuracion[0][21] == 0 else True
        settings.print_cash_receipt=configuracion[0][22]
        imprimir_cuadre=False if configuracion[0][22] == 0 else True
        settings.printer=configuracion[0][23]
        impresora=configuracion[0][23]
        settings.paper_width=configuracion[0][24]
        papel=configuracion[0][24]

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

    btn_cuadre=ft.ElevatedButton(text="Cuadre de caja", icon=ft.icons.ATTACH_MONEY_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=cash_register)

    registros=selectCashRegister()
    if registros != []:
        tblCuadre.height=344
    
    if settings.tipo_app == 0:
        body=ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Stack([
                        ft.Row([
                            ft.Column([
                                ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                                ft.Row([
                                    ft.Icon(ft.icons.ATTACH_MONEY_SHARP, size=32),
                                    ft.Text("Cuadre de caja", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                                ], width=300, alignment=ft.MainAxisAlignment.CENTER)
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
    else:
        btn_home=ft.FilledButton("Inicio".ljust(21, " "), icon=ft.icons.HOME, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/"))
        btn_users=ft.FilledButton("Usuarios".ljust(18, " "), icon=ft.icons.PERSON_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/users"))
        btn_settings=ft.FilledButton("Configuración", icon=ft.icons.SETTINGS, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/configuration"))
        btn_variables=ft.FilledButton("Variables".ljust(18, " "), icon=ft.icons.FACT_CHECK, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/variables"))
        btn_register=ft.FilledButton("Registro".ljust(18, " "), icon=ft.icons.EDIT_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/register"))
        btn_cash_register=ft.FilledButton("Cuadre de caja", icon=ft.icons.ATTACH_MONEY_SHARP, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/cash_register"))
        btn_closing_day=ft.FilledButton("Cierre de día".ljust(18, " "), icon=ft.icons.CALENDAR_MONTH, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/closing_day"))
        btn_developer=ft.FilledButton("Desarrollador".ljust(16, " "), icon=ft.icons.CODE_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/developer"))
        btn_logout=ft.FilledButton("Cerrar sesión".ljust(16, " "), icon=ft.icons.POWER_SETTINGS_NEW, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/login"))
                
        body=ft.Column(
            controls=[
                ft.Row([
                    ft.Container(
                        height=938,
                        width=200,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.colors.BLUE_GREY_300,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        # expand=2,
                        padding=ft.padding.only(0, 20, 0, 0),
                        bgcolor=ft.colors.BLUE_900,
                        border_radius=ft.border_radius.all(10),
                        # alignment=ft.alignment.center,
                        content=ft.Column([
                            # btn_profile,
                            ft.Container(
                                padding=ft.padding.only(10, 10, 10, 10),
                                on_click=lambda e: settings.page.go("/profile"),
                                content=ft.Row([
                                    settings.user_avatar,
                                    # settings.page.user_auth
                                ]),
                            ),
                            ft.Divider(thickness=2),
                            btn_home,
                            btn_users,
                            btn_settings,
                            btn_variables,
                            btn_register,
                            btn_cash_register,
                            btn_closing_day,
                            ft.Divider(thickness=2),
                            btn_developer,
                            ft.Divider(thickness=2),
                            btn_logout
                        ],
                        horizontal_alignment="center",
                        ),
                    ),
                    ft.Container(
                        height=938,
                        expand=10,
                        padding=ft.padding.only(0, 20, 0, 0),
                        # bgcolor="blue",
                        content=ft.Column(
                            controls=[
                                ft.Container(height=20),
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Stack([
                                        ft.Row([
                                            ft.Column([
                                                ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                                                ft.Row([
                                                    ft.Icon(ft.icons.ATTACH_MONEY_SHARP, size=32),
                                                    ft.Text("Cuadre de caja", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                                                ], width=300, alignment=ft.MainAxisAlignment.CENTER)
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
                    )
                ]),
            ]
        )

    return body