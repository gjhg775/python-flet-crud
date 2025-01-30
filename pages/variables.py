import flet as ft
import settings
import sqlite3
from datatable import get_variables, update_variables, get_configuration

# conn=sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
message=""

# class Variables(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#         self.variables=get_variables()

#         if self.variables != None:
#             self.id=self.variables[0][0]
#             self.valor_hora_moto=self.variables[0][1]
#             self.valor_turno_moto=self.variables[0][2]
#             self.valor_hora_carro=self.variables[0][3]
#             self.valor_turno_carro=self.variables[0][4]
#             self.valor_hora_otro=self.variables[0][5]
#             self.valor_turno_otro=self.variables[0][6]

#         def validateVariables(e):
#             self.vlr_hora_moto.error_text=""
#             self.vlr_turno_moto.error_text=""
#             self.vlr_hora_carro.error_text=""
#             self.vlr_turno_carro.error_text=""
#             self.vlr_hora_otro.error_text=""
#             self.vlr_turno_otro.error_text=""
#             if self.vlr_hora_moto.value == "":
#                 self.vlr_hora_moto.error_text="Campo requerido"
#                 # self.vlr_hora_moto.focus()
#                 self.btn_save.focus()
#                 self.vlr_hora_moto.update()
#             else:
#                 self.vlr_hora_moto.update()
#             if self.vlr_turno_moto.value == "":
#                 self.vlr_turno_moto.error_text="Campo requerido"
#                 # self.vlr_turno_moto.focus()
#                 self.vlr_turno_moto.update()
#             if self.vlr_hora_carro.value == "":
#                 self.vlr_hora_carro.error_text="Campo requerido"
#                 # self.vlr_hora_carro.focus()
#                 self.vlr_hora_carro.update()
#             if self.vlr_turno_carro.value == "":
#                 self.vlr_turno_carro.error_text="Campo requerido"
#                 # self.vlr_turno_carro.focus()
#                 self.vlr_turno_carro.update()
#             if self.vlr_hora_otro.value == "":
#                 self.vlr_hora_otro.error_text="Campo requerido"
#                 # self.vlr_hora_otro.focus()
#                 self.vlr_hora_otro.update()
#             if self.vlr_turno_otro.value == "":
#                 self.vlr_turno_otro.error_text="Campo requerido"
#                 # self.vlr_turno_otro.focus()
#                 self.vlr_turno_otro.update()
#             self.btn_save.focus()
#             if self.vlr_hora_moto.value != "" and self.vlr_turno_moto.value != "" and self.vlr_hora_carro.value != "" and self.vlr_turno_carro.value != "" and self.vlr_hora_otro.value != "" and self.vlr_turno_otro.value != "":
#                 self.vlr_hora_moto.update()
#                 self.vlr_turno_moto.update()
#                 self.vlr_hora_carro.update()
#                 self.vlr_turno_carro.update()
#                 self.vlr_hora_otro.update()
#                 self.vlr_turno_otro.update()
#                 update_variables(self.vlr_hora_moto.value, self.vlr_turno_moto.value, self.vlr_hora_carro.value, self.vlr_turno_carro.value, self.vlr_hora_otro.value, self.vlr_turno_otro.value, self.variable_id)

#         self.variable_id=self.id
#         self.vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_hora_moto)
#         self.vlr_turno_moto=ft.TextField(label="Turno Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_turno_moto)
#         self.vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_hora_carro)
#         self.vlr_turno_carro=ft.TextField(label="Turno Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_turno_carro)
#         self.vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_hora_otro)
#         self.vlr_turno_otro=ft.TextField(label="Turno Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_turno_otro)
#         self.btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateVariables)

#     def build(self):
#         return ft.Column(
#             controls=[
#                 ft.Container(height=20),
#                 ft.Container(
#                     alignment=ft.alignment.center,
#                     content=ft.Stack([
#                         ft.Row([
#                             ft.Column([
#                                 ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
#                             ])
#                         ], 
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         ),
#                     ]),
#                 ),
#                 ft.Container(height=10),
#                 ft.Container(
#                     ft.Row([
#                         ft.Column([
#                             self.vlr_hora_moto,
#                             self.vlr_turno_moto,
#                             self.vlr_hora_carro,
#                             self.vlr_turno_carro,
#                             self.vlr_hora_otro,
#                             self.vlr_turno_otro,
#                             self.btn_save
#                         ])
#                     ], 
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                 ),
#             ]
#         )

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
    settings.valor_duplicado=configuracion[0][20]
    valor_duplicado=configuracion[0][20]
    settings.send_email_register=configuracion[0][21]
    enviar_correo_electronico=False if configuracion[0][21] == 0 else True
    settings.email_user=configuracion[0][22]
    correo_usuario=configuracion[0][22]
    settings.email_pass=configuracion[0][23]
    correo_clave=configuracion[0][23]
    settings.secret_key=configuracion[0][24]
    secret_key=configuracion[0][24]
    settings.preview_cash=configuracion[0][25]
    vista_previa_cuadre=False if configuracion[0][25] == 0 else True
    settings.print_cash_receipt=configuracion[0][26]
    imprimir_cuadre=False if configuracion[0][26] == 0 else True
    settings.printer=configuracion[0][27]
    impresora=configuracion[0][27]
    settings.paper_width=configuracion[0][28]
    papel=configuracion[0][28]

def Variables(page):
    variables=get_variables()

    if variables != None:
        id=variables[0][0]
        valor_hora_moto=variables[0][1]
        valor_turno_moto=variables[0][2]
        valor_hora_carro=variables[0][3]
        valor_turno_carro=variables[0][4]
        valor_hora_otro=variables[0][5]
        valor_turno_otro=variables[0][6]

    def validateVariables(e):
        vlr_hora_moto.error_text=""
        vlr_turno_moto.error_text=""
        vlr_hora_carro.error_text=""
        vlr_turno_carro.error_text=""
        vlr_hora_otro.error_text=""
        vlr_turno_otro.error_text=""
        if vlr_hora_moto.value == "":
            vlr_hora_moto.error_text="Campo requerido"
            # vlr_hora_moto.focus()
            btn_save.focus()
            vlr_hora_moto.update()
        else:
            vlr_hora_moto.update()
        if vlr_turno_moto.value == "":
            vlr_turno_moto.error_text="Campo requerido"
            # vlr_turno_moto.focus()
            vlr_turno_moto.update()
        if vlr_hora_carro.value == "":
            vlr_hora_carro.error_text="Campo requerido"
            # vlr_hora_carro.focus()
            vlr_hora_carro.update()
        if vlr_turno_carro.value == "":
            vlr_turno_carro.error_text="Campo requerido"
            # vlr_turno_carro.focus()
            vlr_turno_carro.update()
        if vlr_hora_otro.value == "":
            vlr_hora_otro.error_text="Campo requerido"
            # vlr_hora_otro.focus()
            vlr_hora_otro.update()
        if vlr_turno_otro.value == "":
            vlr_turno_otro.error_text="Campo requerido"
            # vlr_turno_otro.focus()
            vlr_turno_otro.update()
        btn_save.focus()
        if vlr_hora_moto.value != "" and vlr_turno_moto.value != "" and vlr_hora_carro.value != "" and vlr_turno_carro.value != "" and vlr_hora_otro.value != "" and vlr_turno_otro.value != "":
            vlr_hora_moto.update()
            vlr_turno_moto.update()
            vlr_hora_carro.update()
            vlr_turno_carro.update()
            vlr_hora_otro.update()
            vlr_turno_otro.update()
            message=update_variables(vlr_hora_moto.value, vlr_turno_moto.value, vlr_hora_carro.value, vlr_turno_carro.value, vlr_hora_otro.value, vlr_turno_otro.value, variable_id)
            if message != "":
                bgcolor="green"
                settings.message=message
                settings.showMessage(bgcolor)

    variable_id=id
    vlr_hora_moto=ft.TextField(label="Hora Moto", prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_hora_moto)
    vlr_turno_moto=ft.TextField(label="Turno Moto", prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_turno_moto)
    vlr_hora_carro=ft.TextField(label="Hora Carro", prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_hora_carro)
    vlr_turno_carro=ft.TextField(label="Turno Carro", prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_turno_carro)
    vlr_hora_otro=ft.TextField(label="Hora Otro", prefix_icon=ft.icons.VIEW_LIST, value=valor_hora_otro)
    vlr_turno_otro=ft.TextField(label="Turno Otro", prefix_icon=ft.icons.VIEW_LIST, value=valor_turno_otro)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateVariables)

    # if settings.tipo_app == 0:
    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    # ft.Row([
                    #     ft.Column([
                    #         settings.progressRing
                    #     ]),
                    # ], 
                    # alignment=ft.MainAxisAlignment.CENTER,
                    # ),
                    ft.Row([
                        ft.Column([
                            # ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                            # # ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
                            ft.Row([
                                ft.Icon(ft.icons.FACT_CHECK, size=32),
                                ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                            ], width=300, alignment=ft.MainAxisAlignment.CENTER)
                        ])
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(height=10),
            # ft.Container(
            #     ft.Row([
            #         ft.Column([
            #             vlr_hora_moto,
            #             vlr_turno_moto,
            #             vlr_hora_carro,
            #             vlr_turno_carro,
            #             vlr_hora_otro,
            #             vlr_turno_otro,
            #             btn_save
            #         ])
            #     ], 
            #     alignment=ft.MainAxisAlignment.CENTER,
            #     ),
            # ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_moto]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_moto]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_carro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_carro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_otro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_otro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(height=20),
            ft.Container(
                ft.Row([
                    btn_save
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
        ]
    )
    # else:
    #     btn_home=ft.FilledButton("Inicio".ljust(21, " "), icon=ft.icons.HOME, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/"))
    #     btn_users=ft.FilledButton("Usuarios".ljust(18, " "), icon=ft.icons.PERSON_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/users"))
    #     btn_settings=ft.FilledButton("Configuración", icon=ft.icons.SETTINGS, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/configuration"))
    #     btn_variables=ft.FilledButton("Variables".ljust(18, " "), icon=ft.icons.FACT_CHECK, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/variables"))
    #     btn_register=ft.FilledButton("Registro".ljust(18, " "), icon=ft.icons.EDIT_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/register"))
    #     btn_cash_register=ft.FilledButton("Cuadre de caja", icon=ft.icons.ATTACH_MONEY_SHARP, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/cash_register"))
    #     btn_closing_day=ft.FilledButton("Cierre de día".ljust(18, " "), icon=ft.icons.CALENDAR_MONTH, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/closing_day"))
    #     btn_developer=ft.FilledButton("Desarrollador".ljust(16, " "), icon=ft.icons.CODE_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/developer"))
    #     btn_logout=ft.FilledButton("Cerrar sesión".ljust(16, " "), icon=ft.icons.POWER_SETTINGS_NEW, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/login"))

    #     body=ft.Column(
    #         controls=[
    #             ft.Row([
    #                 ft.Container(
    #                     height=938,
    #                     width=200,
    #                     shadow=ft.BoxShadow(
    #                         spread_radius=1,
    #                         blur_radius=15,
    #                         color=ft.colors.BLUE_GREY_300,
    #                         offset=ft.Offset(0, 0),
    #                         blur_style=ft.ShadowBlurStyle.OUTER,
    #                     ),
    #                     # expand=2,
    #                     padding=ft.padding.only(0, 20, 0, 0),
    #                     bgcolor=ft.colors.BLUE_900,
    #                     border_radius=ft.border_radius.all(10),
    #                     # alignment=ft.alignment.center,
    #                     content=ft.Column([
    #                         # btn_profile,
    #                         ft.Container(
    #                             padding=ft.padding.only(10, 10, 10, 10),
    #                             on_click=lambda e: settings.page.go("/profile"),
    #                             content=ft.Row([
    #                                 settings.user_avatar,
    #                                 # settings.page.user_auth
    #                             ]),
    #                         ),
    #                         ft.Divider(thickness=2),
    #                         btn_home,
    #                         btn_users,
    #                         btn_settings,
    #                         btn_variables,
    #                         btn_register,
    #                         btn_cash_register,
    #                         btn_closing_day,
    #                         ft.Divider(thickness=2),
    #                         btn_developer,
    #                         ft.Divider(thickness=2),
    #                         btn_logout
    #                     ],
    #                     horizontal_alignment="center",
    #                     ),
    #                 ),
    #                 ft.Container(
    #                     height=938,
    #                     expand=10,
    #                     padding=ft.padding.only(0, 20, 0, 0),
    #                     # bgcolor="blue",
    #                     content=ft.Column(
    #                         controls=[
    #                             ft.Container(height=20),
    #                             ft.Container(
    #                                 alignment=ft.alignment.center,
    #                                 content=ft.Stack([
    #                                     # ft.Row([
    #                                     #     ft.Column([
    #                                     #         settings.progressRing
    #                                     #     ]),
    #                                     # ], 
    #                                     # alignment=ft.MainAxisAlignment.CENTER,
    #                                     # ),
    #                                     ft.Row([
    #                                         ft.Column([
    #                                             ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
    #                                             # ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
    #                                             ft.Row([
    #                                                 ft.Icon(ft.icons.FACT_CHECK, size=32),
    #                                                 ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
    #                                             ], width=300, alignment=ft.MainAxisAlignment.CENTER)
    #                                         ])
    #                                     ], 
    #                                     alignment=ft.MainAxisAlignment.CENTER,
    #                                     ),
    #                                 ]),
    #                             ),
    #                             ft.Container(height=10),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         ft.Column([
    #                             #             vlr_hora_moto,
    #                             #             vlr_turno_moto,
    #                             #             vlr_hora_carro,
    #                             #             vlr_turno_carro,
    #                             #             vlr_hora_otro,
    #                             #             vlr_turno_otro,
    #                             #             btn_save
    #                             #         ])
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_moto]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_moto]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_carro]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_carro]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_hora_otro]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[vlr_turno_otro]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(height=20),
    #                             ft.Container(
    #                                 ft.Row([
    #                                     btn_save
    #                                 ], 
    #                                 alignment=ft.MainAxisAlignment.CENTER,
    #                                 ),
    #                             ),
    #                         ]
    #                     )
    #                 )
    #             ]),
    #         ]
    #     )
    
    # return body