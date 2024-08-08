import datetime
import locale
import flet as ft
import settings
import sqlite3
from datatable import get_configuration, tblRegistro, tblCuadre

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

def Closing_day(page):
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

    def cancel(e):
        close_dlg(e)
        fecha.value="dd/mm/aaaa"
        fecha.update()

    def close_day(e):
        dia=fecha.value
        if dia != "dd/mm/aaaa":
            title="Cierre de día"
            message="Desea cerrar el día ?"
            open_dlg_modal(e, title, message)
    
    def closing_day(e):
        close_dlg(e)
        dia=fecha.value
        if dia != "dd/mm/aaaa":
            cuadre=1
            cursor=conn.cursor()
            sql=f"""SELECT * FROM registro WHERE strftime('%d/%m/%Y', salida) = '{dia}' AND cuadre = {cuadre}"""
            cursor.execute(sql)
            registros=cursor.fetchall()

            if registros != []:
                message="El día ya fué cerrado con anterioridad"
                bg_color="blue"
            else:
                cuadre=0
                cursor=conn.cursor()
                sql=f"""SELECT * FROM registro WHERE strftime('%d/%m/%Y', salida) = '{dia}' AND cuadre = {cuadre}"""
                cursor.execute(sql)
                registros=cursor.fetchall()

                if registros != []:
                    cuadre=1
                    total=0
                    sql=f"""UPDATE registro SET cuadre = ? WHERE strftime('%d/%m/%Y', salida) <= ? AND total > ?"""
                    values=(f"{cuadre}", f"{dia}", f"{total}")
                    cursor.execute(sql, values)
                    conn.commit()

                    # fecha.value=""
                    # fecha.update()

                    message="Cierre de día realizado satisfactoriamente"
                    bg_color="green"
                    tblRegistro.height=60
                    tblCuadre.height=60
                else:
                    message="Día a cerrar no encontrado ó ya está cerrado. Favor verificar"
                    bg_color="red"

            fecha.value="dd/mm/aaaa"
            fecha.update()
            date_button.focus()

            snack_bar=ft.SnackBar(
                ft.Text(message, color="white", text_align="center"),
                bgcolor=bg_color,
                open=True
            )
            page.overlay.append(snack_bar)
            # page.snack_bar.open=True
            page.update()

    def page_resize(e):
        if page.window.width <= 425:
            settings.textsize=30
        elif page.window.width > 425 and page.window.width <= 678:
            settings.textsize=50
        elif page.window.width >= 768 and page.window.width < 992:
            settings.textsize=70
        elif page.window.width >= 992 and page.window.width <= 1400:
            settings.textsize=90
        if settings.tipo_app == 0:
            fecha.text_size=settings.textsize
        else:
            textsize=settings.textsize
            textsize=settings.textsize
        fecha.update()
        page.update()

    def change_date(e):
        fecha_cierre=str(date_picker.value)
        fecha_cierre=fecha_cierre.split(" ")
        fecha_cierre=fecha_cierre[0]
        fecha_cierre=fecha_cierre.split("-")
        ano=fecha_cierre[0]
        mes=fecha_cierre[1]
        dia=fecha_cierre[2]
        fecha.value=dia + "/" + mes + "/" + ano
        fecha.update()
        # fecha.value=dia + "/" + mes + "/" + ano
        # fecha.focus()
        if settings.tipo_app == 1:
            date_button.focus()
        # print(f"Date picker changed, value is {date_picker.value}")
        close_day(e)

    # def date_picker_dismissed(e):
    #     print(f"Date picker dismissed, value is {date_picker.value}")

    date_picker=ft.DatePicker(
        confirm_text="Aceptar",
        field_label_text="Ingresa una fecha",
        on_change=change_date,
        # on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2024, 7, 1),
        last_date=datetime.datetime(2099, 10, 1),
    )

    page.overlay.append(date_picker)

    date_button=ft.ElevatedButton(
        "Seleccionar fecha",
        icon=ft.icons.CALENDAR_MONTH,
        width=280,
        bgcolor=ft.colors.BLUE_900,
        color="white",
        on_click=lambda _: page.open(date_picker),
    )

    btn_cierre=ft.ElevatedButton(
        text="Cerrar día",
        icon=ft.icons.CALENDAR_MONTH,
        width=280,
        bgcolor=ft.colors.BLUE_900,
        color="white",
        on_click=close_day)

    def close_dlg(e):
        dlg_modal.open=False
        dlg_modal.update()
        # total.update()

    def open_dlg_modal(e, title, message):
        dlg_modal.title=ft.Text(title, text_align="center")
        dlg_modal.content=ft.Text(message, text_align="center")
        dlg_modal.open=True
        # page.overlay.append(dlg_modal)
        dlg_modal.update()

    dlg_modal=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Sí", on_click=closing_day),
            ft.TextButton("No", autofocus=True, on_click=cancel)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda _: date_button.focus(),
    )

    page.overlay.append(dlg_modal)
    
    page.on_resized=page_resize

    if page.window.width <= 425:
        textsize=30
    elif page.window.width > 425 and page.window.width <= 678:
        textsize=50
    elif page.window.width >= 768 and page.window.width < 992:
        textsize=70
    elif page.window.width >= 992:
        textsize=90

    # fecha=ft.TextField(hint_text="dd/mm/aaaa", border="underline", text_size=textsize, width=600, text_align="center", autofocus=True, on_blur=close_day)
    fecha=ft.Text("dd/mm/aaaa", size=textsize, width=600, text_align="center")
    # btn_cierre=ft.ElevatedButton(text="Cerrar día", icon=ft.icons.CALENDAR_MONTH, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=close_day)
    
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
                        ft.Column(col={"xs":12, "sm":12, "md":12, "lg":12, "xl":10, "xxl":8}, controls=[fecha,]),
                        ft.Column(col={"xs":0, "sm":0, "md":0, "lg":0, "xl":1, "xxl":2}),
                    # ]),
                ]),
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    date_button
                ]),
                # content=ft.Row([
                #     date_button,
                #     # btn_cierre
                # ],
                # alignment=ft.alignment.center
                # ),
            ),
        ]
    )