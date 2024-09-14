import time
import datetime
import flet as ft
import settings
import sqlite3
import win32print
from datatable import get_configuration, update_configuration, tbu, tblUsuarios, selectUsers, lblAccesos, tba, tblAccesos

conn=sqlite3.connect("C:/pdb/database/parqueadero.db", check_same_thread=False)
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

def Users(page):
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
        settings.send_email_register=configuracion[0][20]
        enviar_correo=False if configuracion[0][20] == 0 else True
        settings.preview_cash=configuracion[0][21]
        vista_previa_cuadre=False if configuracion[0][21] == 0 else True
        settings.print_cash_receipt=configuracion[0][22]
        imprimir_cuadre=False if configuracion[0][22] == 0 else True
        settings.printer=configuracion[0][23]
        impresora=configuracion[0][23]
        settings.paper_width=configuracion[0][24]
        papel=configuracion[0][24]

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

    lblUsuarios=ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    buscar=ft.TextField(hint_text="Buscar usuario ó nombre", border_radius=50, fill_color=ft.colors.PRIMARY_CONTAINER, filled=True, width=245, text_align="left", autofocus=False, prefix_icon=ft.icons.SEARCH, on_change=search_change)

    registros=selectUsers(search)
    if registros != []:
        if len(registros) < 4:
            tblUsuarios.height=(len(registros)*50)+50
        else:
            tblUsuarios.height=246
        # no_registros.visible=False
    else:
        bgcolor="blue"
        message="No se encontraron registros"
        settings.message=message
        settings.showMessage(bgcolor)

    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.icons.PERSON_ROUNDED, size=32),
                                ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                            ])
                        ]),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(height=10),
            ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
            ft.Container(
                # bgcolor=ft.colors.PRIMARY_CONTAINER,
                # border_radius=10,
                alignment=ft.alignment.center,
                padding=ft.padding.only(10, 0, 10, 0),
                # content=ft.Stack([
                content=ft.ResponsiveRow([
                    # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                    # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros]),
                    # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblAccesos, tblAccesos]),
                    # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":12, "sm":5, "md":6, "lg":5, "xl":5, "xxl":3}, controls=[lblUsuarios, buscar, tblUsuarios], alignment=ft.alignment.center_right),
                    ft.Column(col={"xs":12, "sm":5, "md":5, "lg":5, "xl":3, "xxl":2}, controls=[lblAccesos, tblAccesos]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":3}),
                ]),
                # ]),
            ),
            ft.Container(height=50),
        ]
    )