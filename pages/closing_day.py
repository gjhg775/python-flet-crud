import datetime
import locale
import flet as ft
import settings
import sqlite3
from datatable import get_configuration

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

    def do_nothing(e):
        close_dlg(e)
        fecha.value=""
        fecha.update()

    def close_day(e):
        dia=fecha.value
        if dia != "":
            title="Cierre de día"
            message="Desea cerrar el día ?"
            open_dlg_modal(e, title, message)
    
    def closing_day(e):
        close_dlg(e)
        dia=fecha.value
        if dia != "":
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
                    sql=f"""UPDATE registro SET cuadre = ? WHERE strftime('%d/%m/%Y', salida) = ? AND total > ?"""
                    values=(f"{cuadre}", f"{dia}", f"{total}")
                    cursor.execute(sql, values)
                    conn.commit()

                    fecha.value=""
                    fecha.update()

                    message="Proceso realizado satisfactoriamente"
                    bg_color="green"
                else:
                    message="Día a cerrar no encontrado ó ya está cerrado. Favor verificar"
                    bg_color="red"

            fecha.focus()

            page.snack_bar=ft.SnackBar(
                ft.Text(message, color="white", text_align="center"),
                bgcolor=bg_color
            )
            page.snack_bar.open=True
            page.update()

    def page_resize(e):
        if page.window_width <= 425:
            settings.textsize=30
        elif page.window_width > 425 and page.window_width <= 678:
            settings.textsize=50
        elif page.window_width >= 768 and page.window_width < 992:
            settings.textsize=70
        elif page.window_width >= 992 and page.window_width <= 1400:
            settings.textsize=90
        if settings.sw == 0:
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
        fecha.focus()
        date_button.focus()
        # print(f"Date picker changed, value is {date_picker.value}")

    # def date_picker_dismissed(e):
    #     print(f"Date picker dismissed, value is {date_picker.value}")

    date_picker = ft.DatePicker(
        confirm_text="Aceptar",
        on_change=change_date,
        # on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )

    page.overlay.append(date_picker)

    date_button = ft.ElevatedButton(
        "Seleccionar fecha",
        icon=ft.icons.CALENDAR_MONTH,
        width=280,
        bgcolor=ft.colors.BLUE_900,
        color="white",
        on_click=lambda _: date_picker.pick_date(),
    )

    def close_dlg(e):
        dlg_modal.open=False
        page.update()
        # total.update()

    def open_dlg_modal(e, title, message):
        dlg_modal.title=ft.Text(title, text_align="center")
        dlg_modal.content=ft.Text(message, text_align="center")
        page.dialog=dlg_modal
        dlg_modal.open=True
        page.update()

    dlg_modal=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
        modal=True,
        icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Sí", on_click=closing_day),
            ft.TextButton("No", autofocus=True, on_click=do_nothing)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda _: fecha.focus(),
    )
    
    page.on_resize=page_resize

    if page.window_width <= 425:
        textsize=30
    elif page.window_width > 425 and page.window_width <= 678:
        textsize=50
    elif page.window_width >= 768 and page.window_width < 992:
        textsize=70
    elif page.window_width >= 992:
        textsize=90

    fecha=ft.TextField(hint_text="dd/mm/aaaa", border="underline", text_size=textsize, width=600, text_align="center", autofocus=True, on_blur=close_day)
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
                    # btn_cierre,
                    date_button
                ]),
            ),
        ]
    )