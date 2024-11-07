import os
import sys
import datetime
import time
import locale
import flet as ft
import settings
import sqlite3
import pandas as pd
import re
# from flet import Page
# from app import page
from dotenv import load_dotenv
from decouple import config
from mail import send_mail_billing
from time import sleep
from pages.receipt import show_input, show_output
from datatable import tblRegistro, tb, get_configuration, selectRegisters, selectRegister, exportRegister, update_register_mail, exist_email

# conn=sqlite3.connect("C:/pdb/data/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

if getattr(sys, 'frozen', False):
    # Si está corriendo como un ejecutable
    base_path = sys._MEIPASS
else:
    # Si está corriendo como un script en desarrollo
    base_path = os.path.abspath(".")

# Para acceder a los archivos en assets o upload:
assets_path = os.path.join(base_path, "assets")
# upload_path = os.path.join(base_path, "upload")

# Ejemplo de uso:
# icon_path = os.path.join(assets_path, "img", "parqueadero.png")

# if settings.tipo_app == 0:
#     path=os.path.join(os.getcwd(), "upload\\xls\\")
# else:
#     path=os.path.join(os.getcwd(), "assets\\xls\\")

load_dotenv()

SENDER_EMAIL=os.getenv("EMAIL_USER")
MAIL_PASSWORD=config("EMAIL_PASS")
RECEIVER_EMAIL=settings.correo_electronico

vlr_total=0
vlr_total=locale.currency(vlr_total, grouping=True)
search=""
textsize=settings.textsize

email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

configuracion=get_configuration()

if configuracion != None:
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

# def showInputs(e):
#     variables=get_variables()
#     if variables != None:
#         card.offset=ft.transform.Offset(0,0)
#         placa.focus()
#         page.update()
#     else:
#         title="Variables"
#         message=f"Debe ingresar los valores de las variables"
#         open_dlg_modal(e, title, message)
#         return False

# class Register(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#         self.rdbVehiculo=ft.RadioGroup(
#             content=ft.Row([
#                 # ft.Text("Vehículo", size=20),
#                 ft.Radio(label="Moto", value="Moto"),
#                 ft.Radio(label="Carro", value="Carro"),
#                 ft.Radio(label="Otro", value="Otro")
#             ]),
#             value="Moto",
#             on_change=self.radiogroup_changed
#         )

#         self.dlg_modal=ft.AlertDialog(
#             bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
#             modal=True,
#             icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
#             # title=ft.Text(title, text_align="center"),
#             # content=ft.Text(message, text_align="center"),
#             actions=[
#                 ft.TextButton("Aceptar", autofocus=True, on_click=self.close_dlg)
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             on_dismiss=lambda _: self.placa.focus(),
#         )

#         self.placa=ft.TextField(hint_text="Placa", border="underline", text_size=90, width=600, text_align="center", capitalization="CHARACTERS", autofocus=True, on_blur=self.register)
#         self.total=ft.TextField(hint_text="Total "+str(vlr_total), border="none", text_size=90, width=600, text_align="right", read_only=True)

#         # card=ft.Card(
#         #     margin=ft.margin.only(0, 50, 0, 0),
#         #     offset=ft.transform.Offset(2,0),
#         #     animate_offset=ft.animation.Animation(300, curve="easeIn"),
#         #     elevation=30,
#         #     content=ft.Container(
#         #         ft.Column([
#         #             ft.Row([
#         #                 # ft.Text("Registro", size=20, weight="bold"),
#         #                 ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
#         #                 ft.IconButton(
#         #                     icon="close",
#         #                     icon_size=30,
#         #                     on_click=self.hideInputs
#         #                 ),
#         #             ],
#         #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#         #             ),
#         #             # ft.Row([
#         #             #     ft.Column([
#         #             #         rdbVehiculo,
#         #             #         placa,
#         #             #         total
#         #             #     ])
#         #             # ],
#         #             # alignment=ft.MainAxisAlignment.CENTER
#         #             # # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#         #             # # spacing=20
#         #             # ),
#         #             # ft.Row([
#         #             #     tblRegistro
#         #             #     # lv
#         #             # ],
#         #             # height=268,
#         #             # alignment=ft.MainAxisAlignment.CENTER,
                    
#         #             # # spacing=20
#         #             # ),

#         #             ft.ResponsiveRow([
#         #                 # ft.Column(col=6, controls=[tblRegistro]),
#         #                 ft.Column(col=6, controls=[self.rdbVehiculo, self.placa, self.total])
#         #             ]),

#         #             # ft.Row([
#         #             #     ft.Column([
#         #             #     ft.Text("", size=20, width=530),
#         #             #     ]),
#         #             #     ft.Column([
#         #             #         placa
#         #             #     ]),
#         #             # ],
#         #             # alignment=ft.MainAxisAlignment.END
#         #             # ),
#         #             # ft.Row([
#         #             #     total
#         #             # ],
#         #             # alignment=ft.MainAxisAlignment.END
#         #             # ),
#         #         ]),
#         #         padding=ft.padding.all(10)
#         #     )
#         # )

#     def build(self):
#         return ft.Column(
#             controls=[
#                 ft.Container(height=20),
#                 ft.Container(
#                     alignment=ft.alignment.center,
#                     content=ft.Stack([
#                         ft.Row([
#                             ft.Column([
#                                 ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
#                                 # ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
#                                 # ft.ElevatedButton("Registro", on_click=showInputs)
#                             ])
#                         ], 
#                         alignment=ft.MainAxisAlignment.CENTER,
#                         ),
#                         # ft.ElevatedButton("Inicio", on_click=lambda _:self.page.go("/"), icon=ft.icons.HOME),
#                         # ft.Row([
#                         #     tblRegistro,
#                         #     card
#                         # ]),
#                         # ft.ResponsiveRow([
#                         #     ft.Column(col=6, controls=[tblRegistro]),
#                         #     ft.Column(col=6, controls=[rdbVehiculo, placa, total])
#                         # ]),
#                     ]),
#                 ),
#                 # ft.Container(height=50),
#                 ft.Container(
#                     # bgcolor=ft.colors.PRIMARY_CONTAINER,
#                     # border_radius=10,
#                     alignment=ft.alignment.center,
#                     padding=ft.padding.only(10, 20, 10, 0),
#                     # content=ft.Stack([
#                     content=ft.ResponsiveRow([
#                             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
#                             ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[tblRegistro]),
#                             ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[self.rdbVehiculo, self.placa]),
#                             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
#                         ]),
#                     # ]),
#                 ),
#                 ft.Container(
#                     content=ft.ResponsiveRow([
#                         self.total
#                     ],
#                     alignment=ft.MainAxisAlignment.END
#                     ),
#                 )
#             ]
#             # ft.Container(
#             #     ft.Column([
#             #         ft.Container(
#             #             alignment=ft.alignment.center,
#             #             content=ft.Stack([
#             #                 ft.Image(
#             #                     src=f"img/fondo.jpg",
#             #                     # width=300,
#             #                     # height=300,
#             #                     fit=ft.ImageFit.COVER
#             #                 ),
#             #                 ft.Row([
#             #                     ft.Column([
#             #                         ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
#             #                         # ft.ElevatedButton("Registro", on_click=showInputs)
#             #                         ft.ElevatedButton("Registro")
#             #                     ])
#             #                 ], 
#             #                 alignment=ft.MainAxisAlignment.CENTER
#             #                 ),
#             #                 # ft.Row([
#             #                     # ft.ElevatedButton("Registro", on_click=showInputs),
#             #                     # tblRegistro
#             #                     # card
#             #                 # ]),
#             #                 # card
#             #             ]),
#             #         )
#             #     ])
#             # )
#         )

#     # def hideInputs(self, e):
#     #     self.card.offset=ft.transform.Offset(2,0)
#     #     self.page.update()

#     def register(self, e):
#         if self.placa.value != "":
#             if self.rdbVehiculo.value == "Moto":
#                 for i in self.placa.value:
#                     if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                         if self.rdbVehiculo.value == "Moto" or self.rdbVehiculo.value == "Carro":
#                             if self.rdbVehiculo.value == "Moto":
#                                 message=f"El caracter {i} no es válido para la placa de una moto"
#                             if self.rdbVehiculo.value == "Carro":
#                                 message=f"El caracter {i} no es válido para la placa de un carro"
#                             title="Placa inválida"
#                             self.open_dlg_modal(e, title, message)
#                             return False
#                 if len(self.placa.value) < 5 or len(self.placa.value) > 6:
#                     title="Placa inválida"
#                     message=f"La placa {self.placa.value} no es válida para una moto"
#                     self.open_dlg_modal(e, title, message)
#                     return False
#                 if len(self.placa.value) == 6 and self.placa.value[-1] in "0123456789":
#                     title="Placa inválida"
#                     message=f"La placa {self.placa.value} no es válida para una moto"
#                     self.open_dlg_modal(e, title, message)
#                     return False
#             if self.rdbVehiculo.value == "Carro":
#                 if len(self.placa.value) != 6 or self.placa.value[-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                     title="Placa inválida"
#                     message=f"La placa {self.placa.value} no es válida para un carro"
#                     self.open_dlg_modal(e, title, message)
#                     return False
            
#             vlr_total=selectRegister(self.rdbVehiculo.value, self.placa.value)

#             # print("Total " + str(vlr_total))

#             # if vlr_total == None or vlr_total == "":
#             #     vlr_total = 0

#             if vlr_total == 0:
#                 message="Registro creado satisfactoriamente"
#             else:
#                 message="Registro actualizado satisfactoriamente"

#             self.placa.value=""
#             vlr_total=locale.currency(vlr_total, grouping=True)
#             self.total.hint_text="Total "+str(vlr_total)
#             # card.update()
#             self.total.update()
#             self.placa.focus()
#             tb.rows.clear()
#             selectRegisters()
#             tb.update()
#             tblRegistro.update()

#             # page.snack_bar=ft.SnackBar(
#             #     ft.Text(message, color="white"),
#             #     bgcolor="green"
#             # )
#             # page.snack_bar.open=True
#             # page.update()

#             time.sleep(4)

#             vlr_total=0
#             vlr_total=locale.currency(vlr_total, grouping=True)
#             self.total.hint_text="Total "+str(vlr_total)
#             # card.update()
#             self.total.update()

#     def close_dlg(self, e):
#         self.dlg_modal.open=False
#         self.page.update()
#         self.total.update()

#     def open_dlg_modal(self, e, title, message):
#         self.dlg_modal.title=ft.Text(title, text_align="center")
#         self.dlg_modal.content=ft.Text(message, text_align="center")
#         self.page.dialog=self.dlg_modal
#         self.dlg_modal.open=True
#         self.page.update()

#     def radiogroup_changed(self, e):
#         self.placa.focus()
    
#     selectRegisters()

def Register(page):
    if settings.tipo_app == 0:
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
    
    def register(e):
        if placa.value != "":
            if settings.tipo_app == 1:
                placa.value=e.control.value.upper()
                placa.update()
            buscar.value=""
            if rdbVehiculo.value == "Moto":
                for i in placa.value:
                    if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        if rdbVehiculo.value == "Moto" or rdbVehiculo.value == "Carro":
                            if rdbVehiculo.value == "Moto":
                                message=f"El caracter {i} no es válido para la placa de una moto"
                            if rdbVehiculo.value == "Carro":
                                message=f"El caracter {i} no es válido para la placa de un carro"
                            title="Placa inválida"
                            open_dlg_modal(e, title, message)
                            return False
                if len(placa.value) < 5 or len(placa.value) > 6:
                    title="Placa inválida"
                    message=f"La placa {placa.value} no es válida para una moto"
                    open_dlg_modal(e, title, message)
                    return False
                if len(placa.value) == 6 and placa.value[-1] in "0123456789":
                    title="Placa inválida"
                    message=f"La placa {placa.value} no es válida para una moto"
                    open_dlg_modal(e, title, message)
                    return False
            if rdbVehiculo.value == "Carro":
                if len(placa.value) != 6 or placa.value[-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    title="Placa inválida"
                    message=f"La placa {placa.value} no es válida para un carro"
                    open_dlg_modal(e, title, message)
                    return False
                
            exist_email(placa.value)

            if settings.correo_electronico == "":
                lbl_placa.value=f"Placa {placa.value}"
                lbl_placa.update()
            
            consecutivo, vehiculo, placas, entrada, salida, tiempo, comentario1, comentario2, comentario3, vlr_total, correo_electronico, entradas, salidas=selectRegister(rdbVehiculo.value, placa.value)

            if settings.correcto == 1:
                message="Verifique que la fecha y hora del sistema estén actualizadas"
                bgcolor="red"
                settings.message=message
                settings.showMessage(bgcolor)
                time.sleep(2)
                placa.value=""
                placa.focus()
                placa.update()
                return False
            
            # consecutivo=str(consecutivo).zfill(6) if str(consecutivo[0:1]) == str(settings.prefijo[0:1]) else consecutivo
            consecutivo=str(consecutivo).zfill(6)
            settings.consecutivo2=consecutivo
            
            if comentario1 != "":
                show_input(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, comentario1, comentario2, comentario3, entradas)
            else:
                show_output(parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vehiculo, placas, entrada, salida, tiempo, vlr_total, entradas, salidas)
            
            # print("Total " + str(vlr_total))

            # if vlr_total == None or vlr_total == "":
            #     vlr_total = 0

            settings.placa=placas
            settings.correo_electronico=correo_electronico

            if vlr_total == 0:
                message="Registro creado satisfactoriamente"
                tblRegistro.height=246
            else:
                message="Registro actualizado satisfactoriamente"

            # placa.value=""
            vlr_total=locale.currency(vlr_total, grouping=True)
            total.hint_text="Total "+str(vlr_total)
            # card.update()
            total.update()
            # if settings.tipo_app == 0:
            #     placa.focus()
            tb.rows.clear()
            selectRegisters(search)
            if settings.tipo_app == 0:
                tb.update()
                # tblRegistro.update()
                page.update()
            else:
                settings.page.update()

            bgcolor="green"
            settings.message=message
            settings.showMessage(bgcolor)

            time.sleep(2)

            if settings.send_email_register == 1:
                if settings.correo_electronico == "":
                    open_dlg_modal_email(e)
                else:
                    bgcolor="blue"
                    message="Enviando correo"
                    settings.message=message
                    settings.showMessage(bgcolor)

                    time.sleep(2)

                    settings.progressBar.visible=True
                    if settings.tipo_app == 0:
                        page.open(dlg_modal3)
                        page.update()
                    else:
                        settings.page.open(dlg_modal3)     
                        settings.page.update()

                    send_mail_billing(config("EMAIL_USER"), settings.correo_electronico)

                    settings.progressBar.visible=False
                    if settings.tipo_app == 0:
                        page.close(dlg_modal3)
                        page.update()
                    else:
                        settings.page.close(dlg_modal3)     
                        settings.page.update()

                    bgcolor="green"
                    message="Correo enviado satisfactoriamente"
                    settings.message=message
                    settings.showMessage(bgcolor)

                    time.sleep(2)

            # time.sleep(2)

            placa.value=""
            placa.focus()
            vlr_total=0
            vlr_total=locale.currency(vlr_total, grouping=True)
            total.hint_text="Total "+str(vlr_total)
            # card.update()
            if settings.tipo_app == 0:
                placa.update()
                total.update()
            else:
                settings.page.update()

    def validate_email(e):
        dlg_modal4.content.error_text=""
        email = correo.value
        if not re.match(email_regex, email):
            dlg_modal4.content.error_text="Correo electrónico no válido"
            dlg_modal4.update()
            return False

    def page_resize(e):
        if page.window.width <= 425:
            settings.textsize=30
        elif page.window.width > 425 and page.window.width <= 678:
            settings.textsize=50
        elif page.window.width >= 768 and page.window.width < 992:
            settings.textsize=70
        elif page.window.width >= 992 and page.window.width <= 1400:
            settings.textsize=90
        placa.text_size=settings.textsize
        total.text_size=settings.textsize
        placa.update()
        total.update()
        page.update()

    def close_dlg(e):
        dlg_modal.open=False
        if settings.tipo_app == 0:
            page.update()
            total.update()
        else:
            settings.page.update()

    def open_dlg_modal(e, title, message):
        dlg_modal.title=ft.Row([
            # ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=32),
            ft.Icon(name=ft.icons.WARNING_ROUNDED, size=32),
            ft.Text(title, text_align="center")
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )
        dlg_modal.content=ft.Text(message, text_align="center")
        dlg_modal.open=True
        dlg_modal.update()

    def export_excel(e):
        dlg_modal2.open=False
        dlg_modal2.update()
       
        data=exportRegister(fecha_desde.value, fecha_hasta.value)
        if data != []:
            message="Exportando registros"
            bgcolor="blue"
            settings.message=message
            settings.showMessage(bgcolor)
            
            time.sleep(2)

            settings.progressBar.visible=True
            settings.page.open(dlg_modal3)
            settings.page.update()

            time.sleep(2)

            file_name="register.xlsx"
            df=pd.DataFrame(data, columns=["Factura" if settings.billing == 1 else "Recibo", "Placa", "Entrada", "Salida", "Vehiculo", "Valor", "Tiempo", "Total"])
            df.to_excel(f"{assets_path}\\xls\\{file_name}", index=False)

            settings.progressBar.visible=False
            settings.page.close(dlg_modal3)
            settings.page.update()

            message="Registros exportados satisfactoriamente"
            bgcolor="green"
            settings.message=message
            settings.showMessage(bgcolor)

            time.sleep(2)

            os.system(f"start {assets_path}\\xls\\{file_name}")
        else:
            message="No hay registros para exportar"
            bgcolor="blue"
            settings.message=message
            settings.showMessage(bgcolor)

            time.sleep(2)

        fecha_desde.value="dd/mm/aaaa"
        fecha_hasta.value="dd/mm/aaaa"

    def close_dlg2(e):
        fecha_desde.value="dd/mm/aaaa"
        fecha_hasta.value="dd/mm/aaaa"
        dlg_modal2.open=False
        if settings.tipo_app == 0:
            page.update()
            total.update()
        else:
            settings.page.update()

    def open_dlg_modal2(e):
        if settings.username == "Super Admin" or settings.username == "Admin":
            # dlg_modal2.title=ft.Text(title, text_align="center")
            # dlg_modal2.content=ft.Text(message, text_align="center")
            dlg_modal2.open=True
            dlg_modal2.update()
        else:
            message="Acceso no permitido"
            bgcolor="orange"
            settings.message=message
            settings.showMessage(bgcolor)

    def search_blur(e):
        if settings.tipo_app == 1:
            search_data(e)
    
    def search_change(e):
        if settings.tipo_app == 0:
            search_data(e)

    def search_data(e):
        search=e.control.value.upper()
        buscar.value=search
        buscar.update()
        # no_registros.visible=False
        tb.rows.clear()
        registros=selectRegisters(search)
        if registros != []:
            tblRegistro.height=246
            # no_registros.visible=False
        if registros == [] and search != "":
            tblRegistro.height=60
            # no_registros.visible=True
            bgcolor="blue"
            message="No se encontraron registros"
            settings.message=message
            settings.showMessage(bgcolor)
        if settings.tipo_app == 0:
            page.update()
        else:
            settings.page.update()
        # no_registros.update()
    
    def placa_change(e):
        if settings.tipo_app == 0:
            placa.value=e.control.value.upper()
            placa.update()

    def radiogroup_changed(e):
        placa.focus()

    def change_date_from(e):
        fecha_cierre=str(date_picker_from.value)
        fecha_cierre=fecha_cierre.split(" ")
        fecha_cierre=fecha_cierre[0]
        fecha_cierre=fecha_cierre.split("-")
        ano=fecha_cierre[0]
        mes=fecha_cierre[1]
        dia=fecha_cierre[2]
        fecha_desde.value=dia + "/" + mes + "/" + ano
        fecha_desde.update()
        # fecha.value=dia + "/" + mes + "/" + ano
        # fecha.focus()
        if settings.tipo_app == 1:
            date_button_from.focus()
        # print(f"Date picker changed, value is {date_picker.value}")

    def change_date_to(e):
        fecha_cierre=str(date_picker_to.value)
        fecha_cierre=fecha_cierre.split(" ")
        fecha_cierre=fecha_cierre[0]
        fecha_cierre=fecha_cierre.split("-")
        ano=fecha_cierre[0]
        mes=fecha_cierre[1]
        dia=fecha_cierre[2]
        fecha_hasta.value=dia + "/" + mes + "/" + ano
        fecha_hasta.update()
        # fecha.value=dia + "/" + mes + "/" + ano
        # fecha.focus()
        if settings.tipo_app == 1:
            date_button_to.focus()
        # print(f"Date picker changed, value is {date_picker.value}")

    rdbVehiculo=ft.RadioGroup(
        content=ft.Row([
            # ft.Text("Vehículo", size=20),
            ft.Radio(label="Moto", value="Moto"),
            ft.Radio(label="Carro", value="Carro"),
            ft.Radio(label="Otro", value="Otro")
        ]),
        value="Moto",
        on_change=radiogroup_changed
    )

    date_picker_from=ft.DatePicker(
        confirm_text="Aceptar",
        field_label_text="Ingresa una fecha",
        on_change=change_date_from,
        # on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2024, 7, 1),
        last_date=datetime.datetime(2099, 10, 1),
    )

    date_picker_to=ft.DatePicker(
        confirm_text="Aceptar",
        field_label_text="Ingresa una fecha",
        on_change=change_date_to,
        # on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2024, 7, 1),
        last_date=datetime.datetime(2099, 10, 1),
    )

    if settings.tipo_app == 0:
        page.overlay.append(date_picker_from)
        page.overlay.append(date_picker_to)

    if settings.tipo_app == 0:
        page.on_resized=page_resize

        if page.window.width <= 425:
            textsize=30
        elif page.window.width > 425 and page.window.width <= 678:
            textsize=50
        elif page.window.width >= 768 and page.window.width < 992:
            textsize=70
        elif page.window.width >= 992:
            textsize=90
    else:
         textsize=90
    
    if settings.tipo_app == 0:
        buscar=ft.TextField(hint_text="Buscar consecutivo ó placa", border_radius=50, fill_color=ft.colors.PRIMARY_CONTAINER, filled=True, width=252, text_align="left", autofocus=False, capitalization="CHARACTERS", prefix_icon=ft.icons.SEARCH, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9a-zA-Z]", replacement_string=""), on_change=search_change, on_blur=search_blur)
    else:
        buscar=ft.TextField(hint_text="Buscar consecutivo ó placa", border_radius=50, fill_color=ft.colors.PRIMARY_CONTAINER, filled=True, width=252, text_align="left", autofocus=False, prefix_icon=ft.icons.SEARCH, on_change=search_change, on_blur=search_blur)
    export=ft.IconButton(icon=ft.icons.FILE_DOWNLOAD_OUTLINED, on_click=open_dlg_modal2)
    if settings.tipo_app == 0:
        placa=ft.TextField(hint_text="Placa", border="underline", text_size=textsize, width=600, text_align="center", autofocus=True, capitalization="CHARACTERS", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9a-zA-Z]", replacement_string=""), on_change=placa_change, on_blur=register)
    else:
        placa=ft.TextField(hint_text="Placa", border="underline", text_size=textsize, width=600, text_align="center", autofocus=True, on_change=placa_change, on_blur=register)
    total=ft.TextField(hint_text="Total "+str(vlr_total), border="none", text_size=textsize, width=600, text_align="right", autofocus=False, read_only=True)
    fecha_desde=ft.Text("dd/mm/aaaa", size=24, text_align="center")
    fecha_hasta=ft.Text("dd/mm/aaaa", size=24, text_align="center")
    date_button_from=ft.ElevatedButton("Desde", icon=ft.icons.CALENDAR_MONTH, bgcolor=ft.colors.BLUE_900, color="white", on_click=lambda _: page.open(date_picker_from) if settings.tipo_app == 0 else settings.page.open(date_picker_from))
    date_button_to=ft.ElevatedButton("Hasta", icon=ft.icons.CALENDAR_MONTH, bgcolor=ft.colors.BLUE_900, color="white", on_click=lambda _: page.open(date_picker_to) if settings.tipo_app == 0 else settings.page.open(date_picker_to))
    correo=ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL, text_align="left")
    lbl_placa=ft.Text("", size=24, text_align="center")

    dlg_modal=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        # icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda _: placa.focus(),
    )

    dlg_modal2=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        # title=ft.Row([fecha_desde, date_button_from]),
        title=ft.Row([
            ft.Icon(ft.icons.FILE_DOWNLOAD_OUTLINED, size=32),
            ft.Text("Exportar a Excel", text_align="center", color=ft.colors.PRIMARY)
        ],
        alignment=ft.MainAxisAlignment.CENTER
        ),
        content=ft.ResponsiveRow([
            ft.ResponsiveRow([fecha_desde, date_button_from]),
            ft.ResponsiveRow([fecha_hasta, date_button_to])
        ],
        alignment=ft.MainAxisAlignment.START,
        ),
        # icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Aceptar", on_click=export_excel),
            ft.TextButton("Cancelar", autofocus=True, on_click=close_dlg2)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        on_dismiss=lambda _: placa.focus(),
    )

    dlg_modal3=ft.AlertDialog(
        modal=True,
        bgcolor=ft.colors.TRANSPARENT,
        content=ft.Column(
            [ft.ProgressRing(),],
            height=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    def sendMailBilling(e):
        settings.correo_electronico=correo.value
        if settings.correo_electronico != "":
            validate_email(e)

            if dlg_modal4.content.error_text == "":
                # dlg_modal4.content.error_text=""
                # dlg_modal4.content.update()

                close_dlg4(e)

                bgcolor="blue"
                message="Enviando correo"
                settings.message=message
                settings.showMessage(bgcolor)

                time.sleep(2)

                settings.progressBar.visible=True
                if settings.tipo_app == 0:
                    page.open(dlg_modal3)
                    page.update()
                else:
                    settings.page.open(dlg_modal3)     
                    settings.page.update()

                update_register_mail(settings.correo_electronico, settings.placa)
                send_mail_billing(config("EMAIL_USER"), settings.correo_electronico)

                correo.value=""
                correo.update()

                settings.progressBar.visible=False
                if settings.tipo_app == 0:
                    page.close(dlg_modal3)
                    page.update()
                else:
                    settings.page.close(dlg_modal3)     
                    settings.page.update()

                bgcolor="green"
                message="Correo enviado satisfactoriamente"
                settings.message=message
                settings.showMessage(bgcolor)

                time.sleep(2)
        else:
            dlg_modal4.content.error_text="Digite correo electrónico"
            dlg_modal4.content.update()
            # dlg_modal4.update()
            return False

    def close_dlg4(e):
        correo.update()
        dlg_modal4.open=False
        if settings.tipo_app == 0:
            page.update()
        else:
            settings.page.update()

    def open_dlg_modal_email(e):
        dlg_modal4.title=ft.Row([
            ft.Icon(ft.icons.EMAIL, size=32),
            ft.Text("Correo electrónico", text_align="center", color=ft.colors.PRIMARY)
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )
        # dlg_modal4.title=ft.Text("Correo electrónico", text_align="center")
        # dlg_modal4.content=ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL, text_align="left")
        dlg_modal4.open=True
        dlg_modal4.update()

    dlg_modal4=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        # icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        content=correo,
        actions=[
            lbl_placa,
            ft.TextButton("Enviar", autofocus=True, on_click=sendMailBilling)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        # on_dismiss=lambda _: sendMailBilling,
    )

    if settings.tipo_app == 0:
        page.overlay.append(dlg_modal)
        page.overlay.append(dlg_modal2)
        page.overlay.append(dlg_modal3)
        page.overlay.append(dlg_modal4)
    else:
        settings.page.overlay.append(dlg_modal)
        settings.page.overlay.append(dlg_modal2)
        settings.page.overlay.append(dlg_modal3)
        settings.page.overlay.append(dlg_modal4)

    registros=selectRegisters(search)
    if registros != []:
        tblRegistro.height=246
        # no_registros.visible=False
    else:
        tblRegistro.height=60
        # no_registros.visible=True
        bgcolor="blue"
        message="No se encontraron registros"
        settings.message=message
        settings.showMessage(bgcolor)
    if settings.tipo_app == 0:
        page.update()
    else:
        settings.page.update()

    # card=ft.Card(
    #     margin=ft.margin.only(0, 50, 0, 0),
    #     offset=ft.transform.Offset(2,0),
    #     animate_offset=ft.animation.Animation(300, curve="easeIn"),
    #     elevation=30,
    #     content=ft.Container(
    #         ft.Column([
    #             ft.Row([
    #                 # ft.Text("Registro", size=20, weight="bold"),
    #                 ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
    #                 ft.IconButton(
    #                     icon="close",
    #                     icon_size=30,
    #                     on_click=hideInputs
    #                 ),
    #             ],
    #             alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    #             ),
    #             # ft.Row([
    #             #     ft.Column([
    #             #         rdbVehiculo,
    #             #         placa,
    #             #         total
    #             #     ])
    #             # ],
    #             # alignment=ft.MainAxisAlignment.CENTER
    #             # # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    #             # # spacing=20
    #             # ),
    #             # ft.Row([
    #             #     tblRegistro
    #             #     # lv
    #             # ],
    #             # height=268,
    #             # alignment=ft.MainAxisAlignment.CENTER,
                
    #             # # spacing=20
    #             # ),

    #             ft.ResponsiveRow([
    #                 # ft.Column(col=6, controls=[tblRegistro]),
    #                 ft.Column(col=6, controls=[rdbVehiculo, placa, total])
    #             ]),

    #             # ft.Row([
    #             #     ft.Column([
    #             #     ft.Text("", size=20, width=530),
    #             #     ]),
    #             #     ft.Column([
    #             #         placa
    #             #     ]),
    #             # ],
    #             # alignment=ft.MainAxisAlignment.END
    #             # ),
    #             # ft.Row([
    #             #     total
    #             # ],
    #             # alignment=ft.MainAxisAlignment.END
    #             # ),
    #         ]),
    #         padding=ft.padding.all(10)
    #     )
    # )

    # if settings.tipo_app == 0:
    return ft.Column(
        controls=[
            settings.progressBar,
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
                            ft.Row([
                                ft.Icon(ft.icons.EDIT_ROUNDED, size=32),
                                ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                            ], width=300, alignment=ft.MainAxisAlignment.CENTER)
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
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[ft.Container(ft.Row([buscar, export])), tblRegistro]),
                    ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[rdbVehiculo, placa]),
                    ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                ]),
                # ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 10, 0),
                content=ft.ResponsiveRow([
                    total
                ],
                alignment=ft.MainAxisAlignment.END
                ),
            ),
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
    #             settings.progressBar,
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
    #                             # settings.progressBar,
    #                             ft.Container(height=20),
    #                             ft.Container(
    #                                 alignment=ft.alignment.center,
    #                                 content=ft.Stack([
    #                                     ft.Row([
    #                                         ft.Column([
    #                                             ft.Text(parqueadero, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", weight="bold", color=ft.colors.BLUE_900),
    #                                             ft.Row([
    #                                                 ft.Icon(ft.icons.EDIT_ROUNDED, size=32),
    #                                                 ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
    #                                             ], width=300, alignment=ft.MainAxisAlignment.CENTER)
    #                                             # ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
    #                                             # ft.ElevatedButton("Registro", on_click=showInputs)
    #                                         ])
    #                                     ], 
    #                                     alignment=ft.MainAxisAlignment.CENTER,
    #                                     ),
    #                                     # ft.ElevatedButton("Inicio", on_click=lambda _:page.go("/"), icon=ft.icons.HOME),
    #                                     # ft.Row([
    #                                     #     tblRegistro,
    #                                     #     card
    #                                     # ]),
    #                                     # ft.ResponsiveRow([
    #                                     #     ft.Column(col=6, controls=[tblRegistro]),
    #                                     #     ft.Column(col=6, controls=[rdbVehiculo, placa, total])
    #                                     # ]),
    #                                 ]),
    #                             ),
    #                             # ft.Container(height=50),
    #                             ft.Container(
    #                                 # bgcolor=ft.colors.PRIMARY_CONTAINER,
    #                                 # border_radius=10,
    #                                 alignment=ft.alignment.center,
    #                                 padding=ft.padding.only(10, 20, 10, 0),
    #                                 # content=ft.Stack([
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[ft.Container(ft.Row([buscar, export])), tblRegistro]),
    #                                     ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[rdbVehiculo, placa]),
    #                                     ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
    #                                 ]),
    #                                 # ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 10, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     total
    #                                 ],
    #                                 alignment=ft.MainAxisAlignment.END
    #                                 ),
    #                             ),
    #                         ]
    #                     )
    #                 )
    #             ]),
    #         ]
    #     )

    # return body

# selectRegisters(search)




# import time
# import locale
# import flet as ft
# from flet import Page
# from datatable import tblRegistro, tb, get_configuration, get_variables, selectRegisters, selectRegister
# import sqlite3

# conn=sqlite3.connect("data/parqueadero.db", check_same_thread=False)

# locale.setlocale(locale.LC_ALL, "")

# class Register:

#     # def __init__(self):

#     def main(page:Page):
#         # page.scroll="auto"

#         vlr_total=0
#         vlr_total=locale.currency(vlr_total, grouping=True)

#         parqueadero, regimen=get_configuration()

#         def showInputs(e):
#             variables=get_variables()
#             if variables != None:
#                 card.offset=ft.transform.Offset(0,0)
#                 placa.focus()
#                 page.update()
#             else:
#                 title="Variables"
#                 message=f"Debe ingresar los valores de las variables"
#                 open_dlg_modal(e, title, message)
#                 return False

#         def hideInputs(e):
#             card.offset=ft.transform.Offset(2,0)
#             page.update()

#         def register(e):
#             if placa.value != "":
#                 if rdbVehiculo.value == "Moto":
#                     if len(placa.value) < 5 or len(placa.value) > 6:
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para una moto"
#                         open_dlg_modal(e, title, message)
#                         return False
#                     if len(placa.value) == 6 and placa.value[-1] in "0123456789":
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para una moto"
#                         open_dlg_modal(e, title, message)
#                         return False
#                 if rdbVehiculo.value == "Carro":
#                     if len(placa.value) != 6 or placa.value[-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para un carro"
#                         open_dlg_modal(e, title, message)
#                         return False
#                 for i in placa.value:
#                     if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                         if rdbVehiculo.value == "Moto" or rdbVehiculo.value == "Carro":
#                             if rdbVehiculo.value == "Moto":
#                                 message=f"El caracter {i} no es válido para la placa de una moto"
#                             if rdbVehiculo.value == "Carro":
#                                 message=f"El caracter {i} no es válido para la placa de un carro"
#                             title="Placa inválida"
#                             open_dlg_modal(e, title, message)
#                             return False
#                 vlr_total=selectRegister(rdbVehiculo.value, placa.value)

#                 if vlr_total == None:
#                     vlr_total = 0

#                 if vlr_total == 0:
#                     message="Registro creado satisfactoriamente"
#                 else:
#                     message="Registro actualizado satisfactoriamente"

#                 placa.value=""
#                 vlr_total=locale.currency(vlr_total, grouping=True)
#                 total.hint_text="Total "+str(vlr_total)
#                 card.update()
#                 placa.focus()
#                 tb.rows.clear()
#                 selectRegisters()
#                 tb.update()

#                 page.snack_bar=ft.SnackBar(
#                     ft.Text(message, color="white"),
#                     bgcolor="green"
#                 )
#                 page.snack_bar.open=True
#                 page.update()

#                 time.sleep(4)

#                 vlr_total=0
#                 vlr_total=locale.currency(vlr_total, grouping=True)
#                 total.hint_text="Total "+str(vlr_total)
#                 card.update()

#         def close_dlg(e):
#             dlg_modal.open=False
#             page.update()

#         def open_dlg_modal(e, title, message):
#             dlg_modal.title=ft.Text(title, text_align="center")
#             dlg_modal.content=ft.Text(message, text_align="center")
#             page.dialog=dlg_modal
#             dlg_modal.open=True
#             page.update()

#         def radiogroup_changed(e):
#             placa.focus()

#         rdbVehiculo=ft.RadioGroup(
#             content=ft.Row([
#                 # ft.Text("Vehículo", size=20),
#                 ft.Radio(label="Moto", value="Moto"),
#                 ft.Radio(label="Carro", value="Carro"),
#                 ft.Radio(label="Otro", value="Otro")
#             ]),
#             value="Moto",
#             on_change=radiogroup_changed
#         )

#         dlg_modal=ft.AlertDialog(
#             bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
#             modal=True,
#             icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
#             # title=ft.Text(title, text_align="center"),
#             # content=ft.Text(message, text_align="center"),
#             actions=[
#                 ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg)
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             on_dismiss=lambda e: placa.focus(),
#         )
        
#         placa=ft.TextField(hint_text="Placa", border="underline", text_size=90, width=600, text_align="center", capitalization="CHARACTERS", on_blur=register)
#         total=ft.TextField(hint_text="Total "+str(vlr_total), border="none", text_size=65, width=600, text_align="right", read_only=True)

#         card=ft.Card(
#             margin=ft.margin.only(0, 50, 0, 0),
#             offset=ft.transform.Offset(2,0),
#             animate_offset=ft.animation.Animation(300, curve="easeIn"),
#             elevation=30,
#             content=ft.Container(
#                 ft.Column([
#                     ft.Row([
#                         # ft.Text("Registro", size=20, weight="bold"),
#                         ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
#                         ft.IconButton(
#                             icon="close",
#                             icon_size=30,
#                             on_click=hideInputs
#                         ),
#                     ],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#                     ),
#                     # ft.Row([
#                     #     ft.Column([
#                     #         rdbVehiculo,
#                     #         placa,
#                     #         total
#                     #     ])
#                     # ],
#                     # alignment=ft.MainAxisAlignment.CENTER
#                     # # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#                     # # spacing=20
#                     # ),
#                     # ft.Row([
#                     #     tblRegistro
#                     #     # lv
#                     # ],
#                     # height=268,
#                     # alignment=ft.MainAxisAlignment.CENTER,
                    
#                     # # spacing=20
#                     # ),

#                     ft.ResponsiveRow([
#                         ft.Column(col=6, controls=[tblRegistro]),
#                         ft.Column(col=6, controls=[rdbVehiculo, placa, total])
#                     ]),

#                     # ft.Row([
#                     #     ft.Column([
#                     #     ft.Text("", size=20, width=530),
#                     #     ]),
#                     #     ft.Column([
#                     #         placa
#                     #     ]),
#                     # ],
#                     # alignment=ft.MainAxisAlignment.END
#                     # ),
#                     # ft.Row([
#                     #     total
#                     # ],
#                     # alignment=ft.MainAxisAlignment.END
#                     # ),
#                 ]),
#                 padding=ft.padding.all(10)
#             )
#         )

#         container=ft.Container(
#             ft.Column([
#                 ft.Container(
#                     alignment=ft.alignment.center,
#                     content=ft.Stack([
#                         ft.Image(
#                             src=f"img/fondo.jpg",
#                             # width=300,
#                             # height=300,
#                             fit=ft.ImageFit.COVER
#                         ),
#                         ft.Row([
#                             ft.Column([
#                                 ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold")
#                                 # ft.ElevatedButton("Registro", on_click=showInputs)
#                             ])
#                         ], 
#                         alignment=ft.MainAxisAlignment.CENTER
#                         ),
#                         # ft.Row([
#                             ft.ElevatedButton("Registro", on_click=showInputs),
#                             # tblRegistro
#                             card
#                         # ]),
#                         # card
#                     ]),
#                 )
#             ])
#         )

#         page.window_always_on_top=True
#         page.window_maximizable=False
#         page.window_resizable=False
#         # page.window_height=600
#         # page.window_width=800
#         # page.window_center()
#         # page.window_bgcolor=ft.colors.TRANSPARENT
#         page.window_opacity=0.8
#         # page.bgcolor=ft.colors.TRANSPARENT
#         page.opacity=0.0
#         page.title="Parqueadero"
#         # page.window_maximized=True
#         page.vertical_alignment="center"
#         page.horizontal_alignment="center"
#         page.add(container)
#         page.update()

#         showInputs
#         selectRegisters()
#         tblRegistro.scroll="auto"
#         tblRegistro.update()
        
#     # ft.app(target=main)
#     # ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9000)