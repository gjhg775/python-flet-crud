import os
import time
import datetime
import flet as ft
import settings
import secrets
import sqlite3
import win32print
from flet.security import encrypt
from datatable import get_configuration, update_configuration, tbu, tblUsuarios, selectUsers, lblAccesos, tba, tblAccesos
from dotenv import load_dotenv

load_dotenv()

# conn=sqlite3.connect("C:/pdb/data/parqueadero.db", check_same_thread=False)
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
        settings.send_email_register=configuracion[0][20]
        enviar_correo_electronico=False if configuracion[0][20] == 0 else True
        settings.email_user=configuracion[0][21]
        correo_usuario=configuracion[0][21]
        settings.email_pass=configuracion[0][22]
        correo_clave=configuracion[0][22]
        settings.secret_key=configuracion[0][23]
        secret_key=configuracion[0][23]
        settings.preview_cash=configuracion[0][24]
        vista_previa_cuadre=False if configuracion[0][24] == 0 else True
        settings.print_cash_receipt=configuracion[0][25]
        imprimir_cuadre=False if configuracion[0][25] == 0 else True
        settings.printer=configuracion[0][26]
        impresora=configuracion[0][26]
        settings.paper_width=configuracion[0][27]
        papel=configuracion[0][27]

    def validateConfiguration(e):
        parqueadero.error_text=""
        nit.error_text=""
        regimen.error_text=""
        direccion.error_text=""
        telefono.error_text=""
        servicio.error_text=""
        resolucion.error_text=""
        fecha_desde.error_text=""
        fecha_hasta.error_text=""
        prefijo.error_text=""
        autoriza_del.error_text=""
        autoriza_al.error_text=""
        clave_tecnica.error_text=""
        environment.error_text=""
        client.error_text=""
        consecutivo.error_text=""
        email_user.error_text=""
        email_pass.error_text=""
        printer.error_text=""
        paper_width.error_text=""
        settings.errors=0
        if parqueadero.value == "":
            settings.errors=1
            parqueadero.error_text="Campo requerido"
            btn_save.focus()
            parqueadero.update()
        else:
            parqueadero.update()
        if nit.value == "":
            settings.errors=1
            nit.error_text="Campo requerido"
            nit.update()
        else:
            nit.update()
        if regimen.value == "":
            settings.errors=1
            regimen.error_text="Campo requerido"
            regimen.update()
        else:
            regimen.update()
        if direccion.value == "":
            settings.errors=1
            direccion.error_text="Campo requerido"
            direccion.update()
        else:
            direccion.update()
        if telefono.value == "":
            settings.errors=1
            telefono.error_text="Campo requerido"
            telefono.update()
        else:
            telefono.update()
        if servicio.value == "":
            settings.errors=1
            servicio.error_text="Campo requerido"
            servicio.update()
        else:
            servicio.update()
        if settings.billing == 1:
            if resolucion.value == "":
                settings.errors=1
                resolucion.error_text="Campo requerido"
                resolucion.update()
            else:
                resolucion.update()
            if prefijo.value == "":
                settings.errors=1
                prefijo.error_text="Campo requerido"
                prefijo.update()
            else:
                prefijo.update()
            if fecha_desde.value == "":
                settings.errors=1
                fecha_desde.error_text="Campo requerido"
                fecha_desde.update()
            else:
                fecha_desde.update()
            if fecha_hasta.value == "":
                settings.errors=1
                fecha_hasta.error_text="Campo requerido"
                fecha_hasta.update()
            else:
                fecha_hasta.update()
            if autoriza_del.value == "":
                settings.errors=1
                autoriza_del.error_text="Campo requerido"
                autoriza_del.update()
            else:
                autoriza_del.update()
            if autoriza_al.value == "":
                settings.errors=1
                autoriza_al.error_text="Campo requerido"
                autoriza_al.update()
            else:
                autoriza_al.update()
            if clave_tecnica.value == "":
                settings.errors=1
                clave_tecnica.error_text="Campo requerido"
                clave_tecnica.update()
            else:
                clave_tecnica.update()
            if environment.value == 0:
                settings.errors=1
                environment.error_text="Campo requerido"
                environment.update()
            else:
                environment.update()
            if client.value == 0:
                settings.errors=1
                client.error_text="Campo requerido"
                client.update()
            else:
                client.update()
        if consecutivo.value == "":
            settings.errors=1
            consecutivo.error_text="Campo requerido"
            consecutivo.update()
        else:
            consecutivo.update()
        if settings.send_email_register == 1:
            if email_user.value == "":
                settings.errors=1
                email_user.error_text="Campo requerido"
                email_user.update()
            else:
                email_user.update()
            if email_pass.value == "":
                settings.errors=1
                email_pass.error_text="Campo requerido"
                email_pass.update()
            else:
                email_pass.update()
        if settings.print_register_receipt == 1 or settings.print_cash_receipt == 1:
            if printer.value == "":
                settings.errors=1
                printer.error_text="Campo requerido"
                printer.update()
            else:
                printer.update()
            if paper_width.value == 0:
                settings.errors=1
                paper_width.error_text="Campo requerido"
                paper_width.update()
            else:
                paper_width.update()
        btn_save.focus()
        # if settings.billing == 1:
            # if parqueadero.value != "" and nit.value != "" and regimen.value != "" and direccion.value != "" and telefono.value != "" and servicio.value != "" and resolucion.value != "" and prefijo.value != "" and fecha_desde.value != "" and fecha_hasta.value != "" and autoriza_del.value != "" and autoriza_al.value != "" and clave_tecnica.value != "" and environment.value != "" and client.value != "" and consecutivo.value != "":
        if settings.errors == 0:
            parqueadero.update()
            nit.update()
            regimen.update()
            direccion.update()
            telefono.update()
            servicio.update()
            resolucion.update()
            prefijo.update()
            fecha_desde.update()
            fecha_hasta.update()
            autoriza_del.update()
            autoriza_al.update()
            clave_tecnica.update()
            environment.update()
            client.update()
            consecutivo.update()
            email_user.update()
            email_pass.update()
            if len(email_pass.value) <= 16:
                settings.secret_key=secrets.token_hex(16)
                email_pass_encrypted=encrypt(email_pass.value, settings.secret_key)
                email_pass.value=email_pass_encrypted
                email_pass.update()
            update_configuration(parqueadero.value, nit.value, regimen.value, direccion.value, telefono.value, servicio.value, settings.billing, resolucion.value, fecha_desde.value, fecha_hasta.value, prefijo.value, autoriza_del.value, autoriza_al.value, clave_tecnica.value, environment.value, client.value, consecutivo.value, settings.preview_register, settings.print_register_receipt, settings.send_email_register, email_user.value, email_pass.value, settings.secret_key, settings.preview_cash, settings.print_cash_receipt, printer.value, paper_width.value, configuracion_id)
                # if message != "":
                #     bgcolor="green"
                #     settings.message=message
                #     settings.showMessage(bgcolor)
        # else:
        #     if parqueadero.value != "" and nit.value != "" and regimen.value != "" and direccion.value != "" and telefono.value != "" and servicio.value != "":
        #         parqueadero.update()
        #         nit.update()
        #         regimen.update()
        #         direccion.update()
        #         telefono.update()
        #         servicio.update()
        #         resolucion.update()
        #         prefijo.update()
        #         fecha_desde.update()
        #         fecha_hasta.update()
        #         autoriza_del.update()
        #         autoriza_al.update()
        #         clave_tecnica.update()
        #         environment.update()
        #         client.update()
        #         consecutivo.update()
        #         message=update_configuration(parqueadero.value, nit.value, regimen.value, direccion.value, telefono.value, servicio.value, settings.billing, resolucion.value, fecha_desde.value, fecha_hasta.value, prefijo.value, autoriza_del.value, autoriza_al.value, clave_tecnica.value, environment.value, settings.cliente_final, consecutivo.value, settings.preview_register, settings.print_register_receipt, settings.send_email_register, settings.preview_cash, settings.print_cash_receipt, printer.value, paper_width.value, configuracion_id)

            bgcolor="green"
            message="Configuración actualizada satisfactoriamente"
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

    # def page_resize(e):
    #     # if page.window_width <= 425:
    #     #     settings.fieldwith=page.window_width - 40
    #     # elif page.window_width > 425 and page.window_width <= 678:
    #     #     settings.fieldwith=page.window_width - 40
    #     # elif page.window_width >= 768 and page.window_width < 992:
    #     #     settings.fieldwith=page.window_width - 40
    #     # elif page.window_width >= 992 and page.window_width <= 1400:
    #     #     settings.fieldwith=800
    #     # elif page.window_width >= 1200:
    #     #     settings.fieldwith=900
    #     # elif page.window_width >= 1400:
    #     #     settings.fieldwith=1000
    #     if page.window.width < 576:
    #         fieldwith=page.window.width - 40
    #     elif page.window.width >= 576 and page.window.width < 768:
    #         fieldwith=page.window.width - 40
    #     elif page.window.width >= 768:
    #         # settings.fieldwith=page.window.width - 40
    #         fieldwith=700
    #     elif page.window.width >= 992:
    #         fieldwith=900
    #     elif page.window.width >= 1200:
    #         fieldwith=1100
    #     elif page.window.width >= 1400:
    #         fieldwith=1300
    #     # if settings.tipo_app == 0:
    #     parqueadero.width=fieldwith
    #     nit.width=fieldwith
    #     regimen.width=fieldwith
    #     direccion.width=fieldwith
    #     telefono.width=fieldwith
    #     servicio.width=fieldwith
    #     resolucion.width=fieldwith
    #     fecha_desde.width=fieldwith
    #     fecha_hasta.width=fieldwith
    #     prefijo.width=fieldwith
    #     autoriza_del.width=fieldwith
    #     autoriza_al.width=fieldwith
    #     consecutivo.width=fieldwith
    #         # lblDatos.width=settings.fieldwith
    #         # lblUsuarios.width=settings.fieldwith
    #     # else:
    #     #     fieldwith=settings.fieldwith
    #     #     fieldwith=settings.fieldwith
    #     parqueadero.update()
    #     nit.update()
    #     regimen.update()
    #     direccion.update()
    #     telefono.update()
    #     servicio.update()
    #     resolucion.update()
    #     fecha_desde.update()
    #     fecha_hasta.update()
    #     prefijo.update()
    #     autoriza_del.update()
    #     autoriza_al.update()
    #     consecutivo.update()
    #     lblDatos.update()
    #     lblUsuarios.update()
    #     page.update()

    def paper_width_change(e):
        settings.paper_width=e.control.value

    def preview_change(e):
        settings.preview_register=0 if preview_switch.value == False else 1
    
    def print_change(e):
        settings.print_register_receipt=0 if print_receipt_switch.value == False else 1
        printer.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
        paper_width.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
        printer.error_text=""
        paper_width.error_text=""
        printer.update()
        paper_width.update()

    def send_email(e):
        settings.send_email_register=0 if send_receipt_switch.value == False else 1
        email_user.disabled=True if send_receipt_switch.value == False else False
        email_pass.disabled=True if send_receipt_switch.value == False else False
        email_user.error_text=""
        email_pass.error_text=""
        email_user.update()
        email_pass.update()

    def preview_change_cash(e):
        settings.preview_cash=0 if preview_switch_cash.value == False else 1
    
    def print_change_cash(e):
        settings.print_cash_receipt=0 if print_receipt_switch_cash.value == False else 1
        printer.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
        paper_width.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
        printer.error_text=""
        paper_width.error_text=""
        printer.update()
        paper_width.update()

    def client_change(e):
        settings.cliente_final=client.value

    def environment_change(e):
        settings.tipo_ambiente=environment.value

    def billing_change(e):
        settings.billing=0 if billing_switch.value == False else 1
        resolucion.disabled=True if settings.billing == 0 else False
        fecha_desde.disabled=True if settings.billing == 0 else False
        date_button_from.disabled=True if settings.billing == 0 else False
        fecha_hasta.disabled=True if settings.billing == 0 else False
        date_button_to.disabled=True if settings.billing == 0 else False
        prefijo.disabled=True if settings.billing == 0 else False
        autoriza_del.disabled=True if settings.billing == 0 else False
        autoriza_al.disabled=True if settings.billing == 0 else False
        clave_tecnica.disabled=True if settings.billing == 0 else False
        environment.disabled=True if settings.billing == 0 else False
        client.disabled=True if settings.billing == 0 else False
        resolucion.value=settings.resolucion if billing_switch.value == True else ""
        fecha_desde.value=settings.fecha_desde if billing_switch.value == True else ""
        fecha_hasta.value=settings.fecha_hasta if billing_switch.value == True else ""
        prefijo.value=settings.prefijo if billing_switch.value == True else ""
        autoriza_del.value=settings.autoriza_del if billing_switch.value == True else ""
        autoriza_al.value=settings.autoriza_al if billing_switch.value == True else ""
        clave_tecnica.value=settings.clave_tecnica if billing_switch.value == True else ""
        consecutivo.value=settings.consecutivo if billing_switch.value == True else ""
        environment.value=settings.tipo_ambiente if billing_switch.value == True else 0
        client.value=settings.cliente_final if billing_switch.value == True else 0
        # settings.tipo_ambiente=settings.tipo_ambiente if billing_switch.value == True else 0
        # settings.cliente_final=settings.cliente_final if billing_switch.value == True else 0
        resolucion.error_text=""
        fecha_desde.error_text=""
        fecha_hasta.error_text=""
        prefijo.error_text=""
        autoriza_del.error_text=""
        autoriza_al.error_text=""
        clave_tecnica.error_text=""
        environment.error_text=""
        client.error_text=""
        # resolucion.update()
        # fecha_desde.update()
        # date_button_from.update()
        # fecha_hasta.update()
        # date_button_to.update()
        # prefijo.update()
        # autoriza_del.update()
        # autoriza_al.update()
        # clave_tecnica.update()
        # environment.update()
        # client.update()
        settings.page.update()

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

    def autoriza_del_changed(e):
        consecutivo.value = e.control.value
        consecutivo.update()
    
    def prefijo_blur(e):
        prefijo.value=e.control.value.upper()
        settings.page.update()

    def prefijo_change(e):
        prefijo.value=e.control.value.upper()
        prefijo.update()

    # if settings.tipo_app == 0:
    #     page.on_resized=page_resize

    #     # if page.window_width <= 425:
    #     #     fieldwith=page.window_width - 40
    #     # elif page.window_width > 425 and page.window_width <= 678:
    #     #     fieldwith=page.window_width - 40
    #     # elif page.window_width >= 768 and page.window_width < 992:
    #     #     fieldwith=page.window_width - 40
    #     # elif page.window_width >= 992:
    #     #     fieldwith=800
    #     # elif page.window_width >= 1200:
    #     #     fieldwith=900
    #     # elif page.window_width >= 1400:
    #     #     fieldwith=1000
    #     if page.window.width < 576:
    #         fieldwith=page.window.width - 40
    #     elif page.window.width >= 576 and page.window.width < 768:
    #         fieldwith=page.window.width - 40
    #     elif page.window.width >= 768:
    #         # fieldwith=page.window_width - 40
    #         fieldwith=700
    #     elif page.window.width >= 992:
    #         fieldwith=900
    #     elif page.window.width >= 1200:
    #         fieldwith=1100
    #     elif page.window.width >= 1400:
    #         fieldwith=1300

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

    # if settings.tipo_app == 0:
    settings.page.overlay.append(date_picker_from)
    settings.page.overlay.append(date_picker_to)

    configuracion_id=id
    parqueadero=ft.TextField(label="Parqueadero", value=parqueadero)
    nit=ft.TextField(label="NIT", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9-]", replacement_string=""), value=nit)
    regimen=ft.TextField(label="Régimen", value=regimen)
    direccion=ft.TextField(label="Dirección", value=direccion)
    telefono=ft.TextField(label="Teléfono", value=telefono, input_filter=ft.NumbersOnlyInputFilter())
    servicio=ft.TextField(label="Servicio", value=servicio)
    resolucion=ft.TextField(label="Resolución", value=resolucion, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False)
    fecha_desde=ft.TextField(label="Desde", hint_text="dd/mm/aaaa", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9/]", replacement_string=""), value=fecha_desde, read_only=True, disabled=True if settings.billing == 0 else False)
    fecha_hasta=ft.TextField(label="Hasta", hint_text="dd/mm/aaaa", input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9/]", replacement_string=""), value=fecha_hasta, read_only=True, disabled=True if settings.billing == 0 else False)
    date_button_from=ft.ElevatedButton("Desde", icon=ft.icons.CALENDAR_MONTH, width=280, bgcolor=ft.colors.BLUE_900, color="white", disabled=True if settings.billing == 0 else False, on_click=lambda e: settings.page.open(date_picker_from))
    date_button_to=ft.ElevatedButton("Hasta", icon=ft.icons.CALENDAR_MONTH, width=280, bgcolor=ft.colors.BLUE_900, color="white", disabled=True if settings.billing == 0 else False, on_click=lambda e: settings.page.open(date_picker_to))
    if settings.tipo_app == 0:
        prefijo=ft.TextField(label="Prefijo", capitalization="CHARACTERS", input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-Z-]", replacement_string=""), value=prefijo, disabled=True if settings.billing == 0 else False, on_change=prefijo_change)
    else:
        prefijo=ft.TextField(label="Prefijo", capitalization="CHARACTERS", value=prefijo, disabled=True if settings.billing == 0 else False, on_blur=prefijo_blur)
    autoriza_del=ft.TextField(label="Autoriza del", value=autoriza_del, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False, on_change=autoriza_del_changed)
    autoriza_al=ft.TextField(label="Autoriza al", value=autoriza_al, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False)
    clave_tecnica=ft.TextField(label="Clave técnica", value=clave_tecnica, disabled=True if settings.billing == 0 else False)
    consecutivo=ft.TextField(label="Consecutivo", value=consecutivo, input_filter=ft.NumbersOnlyInputFilter())
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=validateConfiguration)
    # lblDatos=ft.Text("Datos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=fieldwith, text_align="left", color=ft.colors.PRIMARY)
    # lblUsuarios=ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=fieldwith, text_align="left", color=ft.colors.PRIMARY)
    lblDatos=ft.Text("Datos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    lblUsuarios=ft.Text("Usuarios", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    # lblAccesos=ft.Text("Accesos", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, width=300, text_align="left", color=ft.colors.PRIMARY)
    buscar=ft.TextField(hint_text="Buscar usuario ó nombre", border_radius=50, fill_color=ft.colors.PRIMARY_CONTAINER, filled=True, width=245, text_align="left", autofocus=False, prefix_icon=ft.icons.SEARCH, on_change=search_change)
    # no_registros=ft.Text("No se encontraron registros", visible=True)
    # btn_cuadre=ft.ElevatedButton(text="Hacer cuadre", icon=ft.icons.APP_REGISTRATION, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=cash_register)
    lblFacturacion=ft.Text("Facturación", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    lbl_billing=ft.Text("Facturación", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    billing_switch=ft.Switch(value=facturacion, on_change=billing_change)
    lblRegistro=ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    # preview_switch=ft.Switch(label="Vista previa", label_position=ft.LabelPosition.LEFT, value=vista_previa, on_change=preview_change)
    # print_receipt_switch=ft.Switch(label="Imprimir", label_position=ft.LabelPosition.LEFT, value=imprimir, on_change=print_change)
    lbl_preview=ft.Text("Vista previa recibo/factura", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    preview_switch=ft.Switch(value=vista_previa_registro, on_change=preview_change)
    lbl_print=ft.Text("Imprimir recibo/factura", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    print_receipt_switch=ft.Switch(value=imprimir_registro, on_change=print_change)
    lbl_send_email=ft.Text("Enviar recibo/factura al correo electrónico", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    send_receipt_switch=ft.Switch(value=enviar_correo_electronico, on_change=send_email)
    email_user=ft.TextField(label="Correo electrónico de Gmail", value=correo_usuario, disabled=True if send_receipt_switch.value == 0 else False)
    email_pass=ft.TextField(label="Contraseña de la aplicación en Google", value=correo_clave, disabled=True if send_receipt_switch.value == 0 else False)
    lblCuadreCaja=ft.Text("Cuadre de Caja", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    lbl_preview_cash=ft.Text("Vista previa recibo", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    preview_switch_cash=ft.Switch(value=vista_previa_cuadre, on_change=preview_change_cash)
    lbl_print_cash=ft.Text("Imprimir recibo", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    print_receipt_switch_cash=ft.Switch(value=imprimir_cuadre, on_change=print_change_cash)

    printers_list=[]
    printers_list.append(ft.dropdown.Option("", "Seleccione impresora", disabled=True))
    printers=[printer[2] for printer in win32print.EnumPrinters(2)]
    for p in printers:
        printers_list.append(ft.dropdown.Option(p),)

    lbl_environment=ft.Text("Ambiente", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    environment=ft.Dropdown(hint_text="Seleccione ambiente", options=[ft.dropdown.Option(0, "Seleccione ambiente", disabled=True), ft.dropdown.Option(1, "Producción"), ft.dropdown.Option(2, "Prueba")], value=tipo_ambiente if settings.billing == 1 else 0, disabled=True if settings.billing == 0 else False, on_change=environment_change)
    lbl_client=ft.Text("Cliente", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    client=ft.Dropdown(hint_text="Seleccione cliente", options=[ft.dropdown.Option(0, "Seleccione cliente", disabled=True), ft.dropdown.Option(222222222222, "Consumidor final")], value=cliente if settings.billing == 1 else 0, disabled=True if settings.billing == 0 else False, on_change=client_change)
    lbl_printer=ft.Text("Impresora", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    printer=ft.Dropdown(hint_text="Seleccione impresora", options=printers_list, value=impresora, disabled=True)
    printer.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
    # papers_list=[{"":"", "58":"58 mm", "80":"80 mm"}]
    lbl_paper_width=ft.Text("Ancho de papel", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    paper_width=ft.Dropdown(hint_text="Seleccione ancho de papel", options=[ft.dropdown.Option(0, "Seleccione ancho de papel", disabled=True), ft.dropdown.Option(58, "58 mm"), ft.dropdown.Option(80, "80 mm")], value=papel, disabled=False, on_change=paper_width_change)
    paper_width.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False

    # registros=selectUsers(search)
    # if registros != []:
    #     if len(registros) < 4:
    #         tblUsuarios.height=(len(registros)*50)+50
    #     else:
    #         tblUsuarios.height=246
    #     # no_registros.visible=False
    # else:
    #     bgcolor="blue"
    #     message="No se encontraron registros"
    #     settings.message=message
    #     settings.showMessage(bgcolor)

    # if message != "":
    #     bgcolor="green"
    #     settings.message=message
    #     settings.showMessage(bgcolor)

    # if settings.tipo_app == 0:
    return ft.Column(
        # height=800,
        # scroll="auto",
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
                            ft.Row([
                                ft.Icon(ft.icons.SETTINGS, size=32),
                                ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
                            ])
                            # ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
                        ]),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(height=10),
            # ft.Container(
            #     padding=ft.padding.only(10, 0, 10, 0),
            #     content=ft.Row([
            #         ft.Column([
            #             lblDatos,
            #             parqueadero,
            #             nit,
            #             regimen,
            #             direccion,
            #             telefono,
            #             servicio,
            #             resolucion,                         
            #         ]),
            #     ],
            #     alignment=ft.MainAxisAlignment.CENTER,
            #     ),
            # ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblDatos, parqueadero]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[nit]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[regimen]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[direccion]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[telefono]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[servicio]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            # ft.Container(
            #     padding=ft.padding.only(0, 0, 20, 0),
            #     content=ft.ResponsiveRow([
            #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
            #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblFacturacion]),
            #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
            #     ]),
            # ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lblFacturacion]),
                    # ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_billing]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[billing_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[resolucion]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[fecha_desde]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                ft.Row([
                    date_button_from
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[fecha_hasta]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                ft.Row([
                    date_button_to
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[prefijo]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[autoriza_del]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[autoriza_al]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[clave_tecnica]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[consecutivo]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lbl_environment, environment, lbl_client, client]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblRegistro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_preview]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[preview_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_print]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[print_receipt_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_send_email]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[send_receipt_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[email_user]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[email_pass]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblCuadreCaja]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_preview_cash]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[preview_switch_cash], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_print_cash]),
                    ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[print_receipt_switch_cash], horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lbl_printer, printer, lbl_paper_width, paper_width]),
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
            ft.Container(height=50),

                # ft.Container(
                #     padding=ft.padding.only(10, 0, 10, 0),
                #     content=ft.Row([
                #         ft.Column([
                #             fecha_desde,
                #         ]),
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     ft.Row([
                #         date_button_from
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(10, 0, 10, 0),
                #     content=ft.Row([
                #         ft.Column([
                #             fecha_hasta, 
                #         ]),
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     ft.Row([
                #         date_button_to
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(10, 0, 10, 0),
                #     content=ft.Row([
                #         ft.Column([
                #             prefijo,
                #             autoriza_del,
                #             autoriza_al,
                #             clave_tecnica,
                #             consecutivo
                #         ]),
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     ft.Row([
                #         btn_save
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
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
                # ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
                # ft.Container(
                #     # bgcolor=ft.colors.PRIMARY_CONTAINER,
                #     # border_radius=10,
                #     alignment=ft.alignment.center,
                #     padding=ft.padding.only(10, 0, 10, 0),
                #     # content=ft.Stack([
                #     content=ft.ResponsiveRow([
                #         # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                #         # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros]),
                #         # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblAccesos, tblAccesos]),
                #         # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":12, "sm":5, "md":6, "lg":5, "xl":5, "xxl":3}, controls=[lblUsuarios, buscar, tblUsuarios], alignment=ft.alignment.center_right),
                #         ft.Column(col={"xs":12, "sm":5, "md":5, "lg":5, "xl":3, "xxl":2}, controls=[lblAccesos, tblAccesos]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":3}),
                #     ]),
                #     # ]),
                # ),
                # ft.Container(height=50),
                # ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
                # ft.Container(
                #     ft.Row([
                #         ft.Column([
                #             lblAjustes,
                #             ft.Row([
                #                 preview_switch,
                #                 lbl_preview,
                #             ]),
                #             ft.Row([
                #                 print_receipt_switch,
                #                 lbl_print,
                #             ]),
                #         ]),
                #     ],
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 10, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblFacturacion]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_billing]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[billing_switch]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
                #         # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
                #         ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[lbl_environment, environment, lbl_client, client]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 10, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblRegistro]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_send_email]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[send_receipt_switch]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 10, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblCuadreCaja]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview_cash]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch_cash]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print_cash]),
                #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch_cash]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(
                #     padding=ft.padding.only(0, 0, 20, 0),
                #     content=ft.ResponsiveRow([
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                #         # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
                #         # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
                #         ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[lbl_printer, printer, lbl_paper_width, paper_width]),
                #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                #     ]),
                # ),
                # ft.Container(height=20),
                # ft.Container(
                #     ft.Row([
                #         btn_save
                #     ], 
                #     alignment=ft.MainAxisAlignment.CENTER,
                #     ),
                # ),
                # ft.Container(height=50),
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
    #                         scroll="auto",
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
    #                                             ft.Row([
    #                                                 ft.Icon(ft.icons.SETTINGS, size=32),
    #                                                 ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, text_align="center", color=ft.colors.PRIMARY)
    #                                             ])
    #                                             # ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
    #                                         ]),
    #                                     ], 
    #                                     alignment=ft.MainAxisAlignment.CENTER,
    #                                     ),
    #                                 ]),
    #                             ),
    #                             ft.Container(height=10),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(10, 0, 10, 0),
    #                             #     content=ft.Row([
    #                             #         ft.Column([
    #                             #             lblDatos,
    #                             #             parqueadero,
    #                             #             nit,
    #                             #             regimen,
    #                             #             direccion,
    #                             #             telefono,
    #                             #             servicio,
    #                             #             resolucion,                         
    #                             #         ]),
    #                             #     ],
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblDatos, parqueadero]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[nit]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[regimen]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[direccion]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[telefono]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[servicio]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                             #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblFacturacion]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                             #     ]),
    #                             # ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lblFacturacion]),
    #                                     # ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_billing]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[billing_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[resolucion]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[fecha_desde]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 ft.Row([
    #                                     date_button_from
    #                                 ], 
    #                                 alignment=ft.MainAxisAlignment.CENTER,
    #                                 ),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[fecha_hasta]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 ft.Row([
    #                                     date_button_to
    #                                 ], 
    #                                 alignment=ft.MainAxisAlignment.CENTER,
    #                                 ),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[prefijo]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[autoriza_del]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[autoriza_al]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[clave_tecnica]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[consecutivo]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lbl_environment, environment, lbl_client, client]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblRegistro]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_preview]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[preview_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_print]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[print_receipt_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_send_email]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[send_receipt_switch], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lblCuadreCaja]),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_preview_cash]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[preview_switch_cash], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":10, "sm":9, "md":9, "lg":9, "xl":9, "xxl":9}, controls=[lbl_print_cash]),
    #                                     ft.Column(col={"xs":2, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}, controls=[print_receipt_switch_cash], horizontal_alignment=ft.CrossAxisAlignment.END),
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                 ]),
    #                             ),
    #                             ft.Container(
    #                                 padding=ft.padding.only(0, 0, 20, 0),
    #                                 content=ft.ResponsiveRow([
    #                                     ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":1}),
    #                                     ft.Column(col={"xs":12, "sm":10, "md":10, "lg":10, "xl":10, "xxl":10}, controls=[lbl_printer, printer, lbl_paper_width, paper_width]),
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
    #                             # ft.Container(height=50),
                                
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(10, 0, 10, 0),
    #                             #     content=ft.Row([
    #                             #         ft.Column([
    #                             #             fecha_desde,
    #                             #         ]),
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         date_button_from
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(10, 0, 10, 0),
    #                             #     content=ft.Row([
    #                             #         ft.Column([
    #                             #             fecha_hasta, 
    #                             #         ]),
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         date_button_to
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(10, 0, 10, 0),
    #                             #     content=ft.Row([
    #                             #         ft.Column([
    #                             #             prefijo,
    #                             #             autoriza_del,
    #                             #             autoriza_al,
    #                             #             clave_tecnica,
    #                             #             consecutivo
    #                             #         ]),
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         btn_save
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     # bgcolor=ft.colors.PRIMARY_CONTAINER,
    #                             #     # border_radius=10,
    #                             #     alignment=ft.alignment.center,
    #                             #     # padding=ft.padding.only(10, 20, 10, 0),
    #                             #     padding=ft.padding.only(10, 25, 10, 0),
    #                             #     content=ft.Stack([
    #                             #     # content=ft.ResponsiveRow([
    #                             #             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
    #                             #             ft.Column(col={"xs":12, "sm":12, "md":12, "lg":12, "xl":10, "xxl":8}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros, lblAccesos, tblAccesos]),
    #                             #             ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
    #                             #         # ]),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
    #                             # ft.Container(
    #                             #     # bgcolor=ft.colors.PRIMARY_CONTAINER,
    #                             #     # border_radius=10,
    #                             #     alignment=ft.alignment.center,
    #                             #     padding=ft.padding.only(10, 0, 10, 0),
    #                             #     # content=ft.Stack([
    #                             #     content=ft.ResponsiveRow([
    #                             #         # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
    #                             #         # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblUsuarios, buscar, tblUsuarios, no_registros]),
    #                             #         # ft.Column(col={"xs":12, "sm":12, "md":6, "lg":6, "xl":6, "xxl":5}, controls=[lblAccesos, tblAccesos]),
    #                             #         # ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":0, "xxl":1}),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":12, "sm":5, "md":6, "lg":5, "xl":5, "xxl":3}, controls=[lblUsuarios, buscar, tblUsuarios], alignment=ft.alignment.center_right),
    #                             #         ft.Column(col={"xs":12, "sm":5, "md":5, "lg":5, "xl":3, "xxl":2}, controls=[lblAccesos, tblAccesos]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":3}),
    #                             #     ]),
    #                             #     # ]),
    #                             # ),
    #                             ft.Container(height=50),
    #                             # ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         ft.Column([
    #                             #             lblAjustes,
    #                             #             ft.Row([
    #                             #                 preview_switch,
    #                             #                 lbl_preview,
    #                             #             ]),
    #                             #             ft.Row([
    #                             #                 print_receipt_switch,
    #                             #                 lbl_print,
    #                             #             ]),
    #                             #         ]),
    #                             #     ],
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 10, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblFacturacion]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_billing]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[billing_switch]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
    #                             #         # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
    #                             #         ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[lbl_environment, environment, lbl_client, client]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 10, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblRegistro]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_send_email]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[send_receipt_switch]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 10, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblCuadreCaja]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview_cash]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch_cash]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print_cash]),
    #                             #         ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch_cash]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(
    #                             #     padding=ft.padding.only(0, 0, 20, 0),
    #                             #     content=ft.ResponsiveRow([
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
    #                             #         # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
    #                             #         # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
    #                             #         ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[lbl_printer, printer, lbl_paper_width, paper_width]),
    #                             #         ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
    #                             #     ]),
    #                             # ),
    #                             # ft.Container(height=20),
    #                             # ft.Container(
    #                             #     ft.Row([
    #                             #         btn_save
    #                             #     ], 
    #                             #     alignment=ft.MainAxisAlignment.CENTER,
    #                             #     ),
    #                             # ),
    #                             # ft.Container(height=50),
    #                         ]
    #                     )
    #                 )
    #             ]),
    #         ]
    #     )

    # return body