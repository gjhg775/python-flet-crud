import time
import flet as ft
import settings
import sqlite3
from datatable import get_configuration, update_configuration, tblUsuarios, tbu, selectUsers, tblAccesos, tba, lblAccesos

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)
search=""
message=""
fieldwith=settings.fieldwith

# class Configuration(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#         self.configuracion=get_configuration()

#         if self.configuracion != None:
#             self.id=self.configuracion[0][0]
#             self.parqueadero=self.configuracion[0][1]
#             self.nit=self.configuracion[0][2]
#             self.regimen=self.configuracion[0][3]
#             self.direccion=self.configuracion[0][4]
#             self.telefono=self.configuracion[0][5]
#             self.servicio=self.configuracion[0][6]
#             self.consecutivo=self.configuracion[0][7]

#         def validateConfiguration(e):
#             self.parqueadero.error_text=""
#             self.nit.error_text=""
#             self.regimen.error_text=""
#             self.direccion.error_text=""
#             self.telefono.error_text=""
#             self.servicio.error_text=""
#             self.consecutivo.error_text=""
#             if self.parqueadero.value == "":
#                 self.parqueadero.error_text="Campo requerido"
#                 self.btn_save.focus()
#                 self.parqueadero.update()
#             else:
#                 self.parqueadero.update()
#             if self.nit.value == "":
#                 self.nit.error_text="Campo requerido"
#                 self.nit.update()
#             else:
#                 self.nit.update()
#             if self.regimen.value == "":
#                 self.regimen.error_text="Campo requerido"
#                 self.regimen.update()
#             else:
#                 self.regimen.update()
#             if self.direccion.value == "":
#                 self.direccion.error_text="Campo requerido"
#                 self.direccion.update()
#             else:
#                 self.direccion.update()
#             if self.telefono.value == "":
#                 self.telefono.error_text="Campo requerido"
#                 self.telefono.update()
#             else:
#                 self.telefono.update()
#             if self.servicio.value == "":
#                 self.servicio.error_text="Campo requerido"
#                 self.servicio.update()
#             else:
#                 self.servicio.update()
#             if self.consecutivo.value == "":
#                 self.consecutivo.error_text="Campo requerido"
#                 self.consecutivo.update()
#             else:
#                 self.consecutivo.update()
#             self.btn_save.focus()
#             if self.parqueadero.value != "" and self.nit.value != "" and self.regimen.value != "" and self.direccion.value != "" and self.telefono.value != "" and self.servicio.value != "" and self.consecutivo.value != "":
#                 self.parqueadero.update()
#                 self.nit.update()
#                 self.regimen.update()
#                 self.direccion.update()
#                 self.telefono.update()
#                 self.servicio.update()
#                 self.consecutivo.update()
#                 update_configuration(self.parqueadero.value, self.nit.value, self.regimen.value, self.direccion.value, self.telefono.value, self.servicio.value, self.consecutivo.value, self.configuracion_id)

#         self.configuracion_id=self.id
#         self.parqueadero=ft.TextField(label="Parqueadero", width=280, value=self.parqueadero)
#         self.nit=ft.TextField(label="Nit", width=280, value=self.nit)
#         self.regimen=ft.TextField(label="Regimen", width=280, value=self.regimen)
#         self.direccion=ft.TextField(label="Dirección", width=280, value=self.direccion)
#         self.telefono=ft.TextField(label="Teléfono", width=280, value=self.telefono)
#         self.servicio=ft.TextField(label="Servicio", width=280, value=self.servicio)
#         self.consecutivo=ft.TextField(label="Consecutivo", width=280, value=self.consecutivo)
#         self.btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateConfiguration)

#     def build(self):
#         return ft.Column(
#             controls=[
#                 ft.Container(height=20),
#                 ft.Container(
#                     alignment=ft.alignment.center,
#                     content=ft.Stack([
#                         ft.Row([
#                             ft.Column([
#                                 ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
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
#                             self.parqueadero,
#                             self.nit,
#                             self.regimen,
#                             self.direccion,
#                             self.telefono,
#                             self.servicio,
#                             self.consecutivo,
#                             self.btn_save
#                         ])
#                     ], 
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                 ),
#             ]
#         )

def Configuration(page):
    configuracion=get_configuration()

    if configuracion != None:
        id=configuracion[0][0]
        parqueadero=configuracion[0][1]
        nit=configuracion[0][2]
        regimen=configuracion[0][3]
        direccion=configuracion[0][4]
        telefono=configuracion[0][5]
        servicio=configuracion[0][6]
        consecutivo=configuracion[0][7]
        settings.preview=configuracion[0][8]
        vista_previa=False if configuracion[0][8] == 0 else True

    def validateConfiguration(e):
        parqueadero.error_text=""
        nit.error_text=""
        regimen.error_text=""
        direccion.error_text=""
        telefono.error_text=""
        servicio.error_text=""
        consecutivo.error_text=""
        if parqueadero.value == "":
            parqueadero.error_text="Campo requerido"
            btn_save.focus()
            parqueadero.update()
        else:
            parqueadero.update()
        if nit.value == "":
            nit.error_text="Campo requerido"
            nit.update()
        else:
            nit.update()
        if regimen.value == "":
            regimen.error_text="Campo requerido"
            regimen.update()
        else:
            regimen.update()
        if direccion.value == "":
            direccion.error_text="Campo requerido"
            direccion.update()
        else:
            direccion.update()
        if telefono.value == "":
            telefono.error_text="Campo requerido"
            telefono.update()
        else:
            telefono.update()
        if servicio.value == "":
            servicio.error_text="Campo requerido"
            servicio.update()
        else:
            servicio.update()
        if consecutivo.value == "":
            consecutivo.error_text="Campo requerido"
            consecutivo.update()
        else:
            consecutivo.update()
        btn_save.focus()
        if parqueadero.value != "" and nit.value != "" and regimen.value != "" and direccion.value != "" and telefono.value != "" and servicio.value != "" and consecutivo.value != "":
            parqueadero.update()
            nit.update()
            regimen.update()
            direccion.update()
            telefono.update()
            servicio.update()
            consecutivo.update()
            message=update_configuration(parqueadero.value, nit.value, regimen.value, direccion.value, telefono.value, servicio.value, consecutivo.value, settings.preview, configuracion_id)
            if message != "":
                bgcolor="green"
                settings.message=message
                settings.showMessage(bgcolor)

    def search_change(e):
        search=e.control.value
        # if search == "":
        #     no_registros.visible=False
        tbu.rows.clear()
        tba.rows.clear()
        selectUsers(search)
        if tbu.rows != []:
            tblUsuarios.height=246
            # no_registros.visible=False
        else:
            tblUsuarios.height=60
            # no_registros.visible=True
            lblAccesos.value="Accesos"
            bgcolor="blue"
            message="No se encontraron registros"
            settings.message=message
            settings.showMessage(bgcolor)
        tblUsuarios.update()
        tblAccesos.update()
        # no_registros.update()

    def page_resize(e):
        # if page.window_width <= 425:
        #     settings.fieldwith=page.window_width - 40
        # elif page.window_width > 425 and page.window_width <= 678:
        #     settings.fieldwith=page.window_width - 40
        # elif page.window_width >= 768 and page.window_width < 992:
        #     settings.fieldwith=page.window_width - 40
        # elif page.window_width >= 992 and page.window_width <= 1400:
        #     settings.fieldwith=800
        # elif page.window_width >= 1200:
        #     settings.fieldwith=900
        # elif page.window_width >= 1400:
        #     settings.fieldwith=1000
        if page.window_width < 576:
            settings.fieldwith=page.window_width - 40
        elif page.window_width >= 576 and page.window_width < 768:
            settings.fieldwith=page.window_width - 40
        elif page.window_width >= 768:
            # settings.fieldwith=page.window_width - 40
            settings.fieldwith=700
        elif page.window_width >= 992:
            settings.fieldwith=900
        elif page.window_width >= 1200:
            settings.fieldwith=1100
        elif page.window_width >= 1400:
            settings.fieldwith=1300
        if settings.sw == 0:
            parqueadero.width=settings.fieldwith
            nit.width=settings.fieldwith
            regimen.width=settings.fieldwith
            direccion.width=settings.fieldwith
            telefono.width=settings.fieldwith
            servicio.width=settings.fieldwith
            consecutivo.width=settings.fieldwith
            # lblDatos.width=settings.fieldwith
            # lblUsuarios.width=settings.fieldwith
        # else:
        #     fieldwith=settings.fieldwith
        #     fieldwith=settings.fieldwith
        parqueadero.update()
        nit.update()
        regimen.update()
        direccion.update()
        telefono.update()
        servicio.update()
        consecutivo.update()
        lblDatos.update()
        lblUsuarios.update()
        page.update()

    def preview_change(e):
        settings.preview=0 if preview_switch.value == False else 1

    page.on_resize=page_resize

    # if page.window_width <= 425:
    #     fieldwith=page.window_width - 40
    # elif page.window_width > 425 and page.window_width <= 678:
    #     fieldwith=page.window_width - 40
    # elif page.window_width >= 768 and page.window_width < 992:
    #     fieldwith=page.window_width - 40
    # elif page.window_width >= 992:
    #     fieldwith=800
    # elif page.window_width >= 1200:
    #     fieldwith=900
    # elif page.window_width >= 1400:
    #     fieldwith=1000
    if page.window_width < 576:
        fieldwith=page.window_width - 40
    elif page.window_width >= 576 and page.window_width < 768:
        fieldwith=page.window_width - 40
    elif page.window_width >= 768:
        # fieldwith=page.window_width - 40
        fieldwith=700
    elif page.window_width >= 992:
        fieldwith=900
    elif page.window_width >= 1200:
        fieldwith=1100
    elif page.window_width >= 1400:
        fieldwith=1300

    configuracion_id=id
    parqueadero=ft.TextField(label="Parqueadero", width=fieldwith, value=parqueadero)
    nit=ft.TextField(label="Nit", width=fieldwith, value=nit)
    regimen=ft.TextField(label="Régimen", width=fieldwith, value=regimen)
    direccion=ft.TextField(label="Dirección", width=fieldwith, value=direccion)
    telefono=ft.TextField(label="Teléfono", width=fieldwith, value=telefono)
    servicio=ft.TextField(label="Servicio", width=fieldwith, value=servicio)
    consecutivo=ft.TextField(label="Consecutivo", width=fieldwith, value=consecutivo)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=validateConfiguration)
    # lblDatos=ft.Text("Datos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=fieldwith, text_align="left", color=ft.colors.PRIMARY)
    # lblUsuarios=ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=fieldwith, text_align="left", color=ft.colors.PRIMARY)
    lblDatos=ft.Text("Datos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    lblUsuarios=ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    # lblAccesos=ft.Text("Accesos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=300, text_align="left", color=ft.colors.PRIMARY)
    buscar=ft.TextField(hint_text="Buscar usuario ó nombre", border_radius=50, fill_color=ft.colors.PRIMARY_CONTAINER, filled=True, width=245, text_align="left", autofocus=False, prefix_icon=ft.icons.SEARCH, on_change=search_change)
    # no_registros=ft.Text("No se encontraron registros", visible=True)
    # btn_cuadre=ft.ElevatedButton(text="Hacer cuadre", icon=ft.icons.APP_REGISTRATION, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=cash_register)
    lblAjustes=ft.Text("Ajustes", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    preview_switch=ft.Switch(label="Vista previa", label_position=ft.LabelPosition.LEFT, value=vista_previa, on_change=preview_change)

    registros=selectUsers(search)
    if registros != []:
        tblUsuarios.height=344
        # no_registros.visible=False
    else:
        bgcolor="blue"
        message="No se encontraron registros"
        settings.message=message
        settings.showMessage(bgcolor)

    # if message != "":
    #     bgcolor="green"
    #     settings.message=message
    #     settings.showMessage(bgcolor)

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
                            ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
                        ]),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(height=10),
            ft.Container(
                ft.Row([
                    ft.Column([
                        lblDatos,
                        parqueadero,
                        nit,
                        regimen,
                        direccion,
                        telefono,
                        servicio,
                        consecutivo,
                        # btn_save
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                ft.Row([
                    btn_save
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            # ft.Container(
            #     # bgcolor=ft.colors.PRIMARY_CONTAINER,
            #     # border_radius=10,
            #     alignment=ft.alignment.center,
            #     # padding=ft.padding.only(10, 20, 10, 0),
            #     padding=ft.padding.only(10, 25, 10, 0),
            #     content=ft.Stack([
            #     # content=ft.ResponsiveRow([
            #             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
            #             ft.Column(col={"xs":12, "sm":12, "md":12, "lg":12, "xl":10, "xxl":8}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros, lblAccesos, tblAccesos]),
            #             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
            #         # ]),
            #     ]),
            # ),
            ft.Container(
                # bgcolor=ft.colors.PRIMARY_CONTAINER,
                # border_radius=10,
                # alignment=ft.alignment.center,
                padding=ft.padding.only(10, 0, 10, 0),
                # content=ft.Stack([
                content=ft.ResponsiveRow([
                    # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                    # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros]),
                    # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblAccesos, tblAccesos]),
                    # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                    ft.Column(col={"xs":0, "sm":0, "md":3, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":12, "sm":12, "md":4, "lg":4, "xl":4, "xxl":2}, controls=[lblUsuarios, buscar, tblUsuarios]),
                    ft.Column(col={"xs":12, "sm":12, "md":3, "lg":3, "xl":3, "xxl":2}, controls=[lblAccesos, tblAccesos]),
                    ft.Column(col={"xs":0, "sm":0, "md":2, "lg":2, "xl":2, "xxl":4}),
                ],
                alignment=ft.MainAxisAlignment.CENTER
                ),
                #     ],
                # alignment=ft.MainAxisAlignment.CENTER
                # ),
            ),
            ft.Container(height=10),
            ft.Container(
                ft.Row([
                    ft.Column([
                        lblAjustes,
                        preview_switch
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(height=100)
        ]
    )