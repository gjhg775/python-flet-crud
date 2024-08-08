import time
import datetime
import flet as ft
import settings
import sqlite3
import win32print
from datatable import get_configuration, update_configuration, tbu, tblUsuarios, selectUsers, lblAccesos, tba, tblAccesos

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
        printer.error_text=""
        paper_width.error_text=""
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
        if settings.billing == 1:
            if resolucion.value == "":
                resolucion.error_text="Campo requerido"
                resolucion.update()
            else:
                resolucion.update()
            if prefijo.value == "":
                prefijo.error_text="Campo requerido"
                prefijo.update()
            else:
                prefijo.update()
            if fecha_desde.value == "":
                fecha_desde.error_text="Campo requerido"
                fecha_desde.update()
            else:
                fecha_desde.update()
            if fecha_hasta.value == "":
                fecha_hasta.error_text="Campo requerido"
                fecha_hasta.update()
            else:
                fecha_hasta.update()
            if autoriza_del.value == "":
                autoriza_del.error_text="Campo requerido"
                autoriza_del.update()
            else:
                autoriza_del.update()
            if autoriza_al.value == "":
                autoriza_al.error_text="Campo requerido"
                autoriza_al.update()
            else:
                autoriza_al.update()
            if clave_tecnica.value == "":
                clave_tecnica.error_text="Campo requerido"
                clave_tecnica.update()
            else:
                clave_tecnica.update()
            if environment.value == 0:
                environment.error_text="Campo requerido"
                environment.update()
            else:
                environment.update()
            if client.value == "":
                client.error_text="Campo requerido"
                client.update()
            else:
                client.update()
        if consecutivo.value == "":
            consecutivo.error_text="Campo requerido"
            consecutivo.update()
        else:
            consecutivo.update()
        if settings.print_register_receipt == 1 or settings.print_cash_receipt == 1:
            if printer.value == "":
                printer.error_text="Campo requerido"
                printer.update()
            else:
                printer.update()
            if paper_width.value == 0:
                paper_width.error_text="Campo requerido"
                paper_width.update()
            else:
                paper_width.update()
        btn_save.focus()
        if parqueadero.value != "" and nit.value != "" and regimen.value != "" and direccion.value != "" and telefono.value != "" and servicio.value != "" and resolucion.value != "" and prefijo.value != "" and fecha_desde.value != "" and fecha_hasta.value != "" and autoriza_del.value != "" and autoriza_al.value != "" and clave_tecnica.value != "" and environment.value != 0 and client.value != "" and consecutivo.value != "":
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
            message=update_configuration(parqueadero.value, nit.value, regimen.value, direccion.value, telefono.value, servicio.value, settings.billing, resolucion.value, fecha_desde.value, fecha_hasta.value, prefijo.value, autoriza_del.value, autoriza_al.value, clave_tecnica.value, environment.value, settings.cliente_final, consecutivo.value, settings.preview_register, settings.print_register_receipt, settings.preview_cash, settings.print_cash_receipt, printer.value, paper_width.value, configuracion_id)
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
        if page.window.width < 576:
            settings.fieldwith=page.window.width - 40
        elif page.window.width >= 576 and page.window.width < 768:
            settings.fieldwith=page.window.width - 40
        elif page.window.width >= 768:
            # settings.fieldwith=page.window.width - 40
            settings.fieldwith=700
        elif page.window.width >= 992:
            settings.fieldwith=900
        elif page.window.width >= 1200:
            settings.fieldwith=1100
        elif page.window.width >= 1400:
            settings.fieldwith=1300
        if settings.tipo_app == 0:
            parqueadero.width=settings.fieldwith
            nit.width=settings.fieldwith
            regimen.width=settings.fieldwith
            direccion.width=settings.fieldwith
            telefono.width=settings.fieldwith
            servicio.width=settings.fieldwith
            resolucion.width=settings.fieldwith
            fecha_desde.width=settings.fieldwith
            fecha_hasta.width=settings.fieldwith
            prefijo.width=settings.fieldwith
            autoriza_del.width=settings.fieldwith
            autoriza_al.width=settings.fieldwith
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
        resolucion.update()
        fecha_desde.update()
        fecha_hasta.update()
        prefijo.update()
        autoriza_del.update()
        autoriza_al.update()
        consecutivo.update()
        lblDatos.update()
        lblUsuarios.update()
        page.update()

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
        page.update()

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

    def prefijo_to_upper(e):
        prefijo.value=e.control.value.upper()
        prefijo.update()

    page.on_resized=page_resize

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
    if page.window.width < 576:
        fieldwith=page.window.width - 40
    elif page.window.width >= 576 and page.window.width < 768:
        fieldwith=page.window.width - 40
    elif page.window.width >= 768:
        # fieldwith=page.window_width - 40
        fieldwith=700
    elif page.window.width >= 992:
        fieldwith=900
    elif page.window.width >= 1200:
        fieldwith=1100
    elif page.window.width >= 1400:
        fieldwith=1300

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

    page.overlay.append(date_picker_from)
    page.overlay.append(date_picker_to)

    configuracion_id=id
    parqueadero=ft.TextField(label="Parqueadero", width=fieldwith, value=parqueadero)
    nit=ft.TextField(label="Nit", width=fieldwith, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9-]", replacement_string=""), value=nit)
    regimen=ft.TextField(label="Régimen", width=fieldwith, value=regimen)
    direccion=ft.TextField(label="Dirección", width=fieldwith, value=direccion)
    telefono=ft.TextField(label="Teléfono", width=fieldwith, value=telefono, input_filter=ft.NumbersOnlyInputFilter())
    servicio=ft.TextField(label="Servicio", width=fieldwith, value=servicio)
    resolucion=ft.TextField(label="Resolución", width=fieldwith, value=resolucion, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False)
    fecha_desde=ft.TextField(label="Desde", hint_text="dd/mm/aaaa", width=fieldwith, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9/]", replacement_string=""), value=fecha_desde, disabled=True if settings.billing == 0 else False)
    fecha_hasta=ft.TextField(label="Hasta", hint_text="dd/mm/aaaa", width=fieldwith, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9/]", replacement_string=""), value=fecha_hasta, disabled=True if settings.billing == 0 else False)
    date_button_from=ft.ElevatedButton("Desde", icon=ft.icons.CALENDAR_MONTH, width=280, bgcolor=ft.colors.BLUE_900, color="white", disabled=True if settings.billing == 0 else False, on_click=lambda _: page.open(date_picker_from))
    date_button_to=ft.ElevatedButton("Hasta", icon=ft.icons.CALENDAR_MONTH, width=280, bgcolor=ft.colors.BLUE_900, color="white", disabled=True if settings.billing == 0 else False, on_click=lambda _: page.open(date_picker_to))
    prefijo=ft.TextField(label="Prefijo", width=fieldwith, capitalization="CHARACTERS", input_filter=ft.InputFilter(allow=True, regex_string=r"[a-zA-Z-]", replacement_string=""), value=prefijo, disabled=True if settings.billing == 0 else False, on_change=prefijo_to_upper)
    autoriza_del=ft.TextField(label="Autoriza del", width=fieldwith, value=autoriza_del, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False, on_change=autoriza_del_changed)
    autoriza_al=ft.TextField(label="Autoriza al", width=fieldwith, value=autoriza_al, input_filter=ft.NumbersOnlyInputFilter(), disabled=True if settings.billing == 0 else False)
    clave_tecnica=ft.TextField(label="Clave técnica", width=fieldwith, value=clave_tecnica, disabled=True if settings.billing == 0 else False)
    consecutivo=ft.TextField(label="Consecutivo", width=fieldwith, value=consecutivo, input_filter=ft.NumbersOnlyInputFilter())
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

    environment=ft.Dropdown(hint_text="Seleccione ambiente", options=[ft.dropdown.Option(0, "Seleccione ambiente", disabled=True), ft.dropdown.Option(1, "Producción"), ft.dropdown.Option(2, "Prueba")], value=tipo_ambiente, disabled=True if settings.billing == 0 else False, on_change=environment_change)
    client=ft.Dropdown(hint_text="Seleccione cliente", options=[ft.dropdown.Option("", "Seleccione cliente", disabled=True), ft.dropdown.Option("222222222222", "Consumidor final")], value=cliente, disabled=True if settings.billing == 0 else False, on_change=client_change)
    printer=ft.Dropdown(hint_text="Seleccione impresora", options=printers_list, value=impresora, disabled=True)
    printer.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False
    # papers_list=[{"":"", "58":"58 mm", "80":"80 mm"}]
    paper_width=ft.Dropdown(hint_text="Seleccione ancho de papel", options=[ft.dropdown.Option(0, "Seleccione ancho de papel", disabled=True), ft.dropdown.Option(58, "58 mm"), ft.dropdown.Option(80, "80 mm")], value=papel, on_change=paper_width_change, disabled=False)
    paper_width.disabled=True if settings.print_register_receipt == 0 and settings.print_cash_receipt == 0 else False

    registros=selectUsers(search)
    if registros != []:
        tblUsuarios.height=246
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
                padding=ft.padding.only(10, 0, 10, 0),
                content=ft.Row([
                    ft.Column([
                        lblDatos,
                        parqueadero,
                        nit,
                        regimen,
                        direccion,
                        telefono,
                        servicio,
                        resolucion
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                padding=ft.padding.only(10, 0, 10, 0),
                content=ft.Row([
                    ft.Column([
                        fecha_desde,
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                ft.Row([
                    date_button_from
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                padding=ft.padding.only(10, 0, 10, 0),
                content=ft.Row([
                    ft.Column([
                        fecha_hasta, 
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                ft.Row([
                    date_button_to
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                padding=ft.padding.only(10, 0, 10, 0),
                content=ft.Row([
                    ft.Column([
                        prefijo,
                        autoriza_del,
                        autoriza_al,
                        clave_tecnica,
                        consecutivo
                    ]),
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
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
                    ft.Column(col={"xs":12, "sm":5, "md":5, "lg":5, "xl":5, "xxl":3}, controls=[lblUsuarios, buscar, tblUsuarios], alignment=ft.alignment.center_right),
                    ft.Column(col={"xs":12, "sm":5, "md":5, "lg":5, "xl":3, "xxl":2}, controls=[lblAccesos, tblAccesos]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":1, "xl":1, "xxl":3}),
                ]),
                # ]),
            ),
            ft.Container(height={"xs":0, "sm":0, "md":10, "lg":100, "xl":100, "xxl":100}),
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
            ft.Container(
                padding=ft.padding.only(0, 0, 10, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblFacturacion]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_billing]),
                    ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[billing_switch]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
                    # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
                    ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[environment, client]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 10, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblRegistro]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview]),
                    ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print]),
                    ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 10, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":12, "sm":10, "md":10, "lg":6, "xl":6, "xxl":4}, controls=[lblCuadreCaja]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_preview_cash]),
                    ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[preview_switch_cash]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_print_cash]),
                    ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[print_receipt_switch_cash]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
                ]),
            ),
            ft.Container(
                padding=ft.padding.only(0, 0, 20, 0),
                content=ft.ResponsiveRow([
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":3, "xl":3, "xxl":4}),
                    # ft.Column(col={"xs":10, "sm":5, "md":5, "lg":4, "xl":4, "xxl":3}, controls=[lbl_printer]),
                    # ft.Column(col={"xs":2, "sm":5, "md":5, "lg":3, "xl":3, "xxl":2}, controls=[ft.Container(ft.Row([lbl_printer, printer]))]),
                    ft.Column(col={"xs":12, "sm":6, "md":6, "lg":4, "xl":4, "xxl":2}, controls=[printer, paper_width]),
                    ft.Column(col={"xs":0, "sm":1, "md":1, "lg":2, "xl":2, "xxl":3}),
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
        ]
    )