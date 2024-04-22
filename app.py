import flet as ft
from flet import Icon
from datatable import tblRegistro, tb, lv, selectRegisters, selectRegister
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

def main(page:ft.Page):
    page.scroll="auto"

    def showInputs(e):
        card.offset=ft.transform.Offset(0,0)
        placa.focus()
        page.update()

    def hideInputs(e):
        card.offset=ft.transform.Offset(2,0)
        page.update()

    def register(e):
        if placa.value != "":
            for i in placa.value:
                if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    open_dlg_modal(e)
                    return False
            if rdbVehiculo.value == "Moto":
                mensaje="La placa no es válida para una moto"
            if rdbVehiculo.value == "Carro":
                mensaje="La placa no es válida para un carro"
            selectRegister(rdbVehiculo.value, placa.value)
            placa.value=""
            placa.focus()
            tb.rows.clear()
            selectRegisters()
            tb.update()

    def close_dlg(e):
        dlg_modal.open=False
        page.update()

    def radiogroup_changed(e):
        # vehiculo=e.control.value
        placa.focus()

    rdbVehiculo=ft.RadioGroup(
        content=ft.Row([
            ft.Text("Vehículo", size=20),
            ft.Radio(label="Moto", value="Moto"),
            ft.Radio(label="Carro", value="Carro"),
            ft.Radio(label="Otro", value="Otro")
        ]),
        on_change=radiogroup_changed
    )

    rdbVehiculo.value="Moto"
    mensaje="La placa no es válida para una moto"

    dlg_modal = ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
        modal=True,
        icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
        title=ft.Text("Placa inválida", text_align="center"),
        content=ft.Text(mensaje, text_align="center"),
        actions=[
            ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: placa.focus(),
    )

    def open_dlg_modal(e):
        page.dialog=dlg_modal
        dlg_modal.open=True
        page.update()
    
    placa=ft.TextField(hint_text="Placa", border="underline", text_size=90, width=600, text_align="center", capitalization="CHARACTERS", on_blur=register)
    # total=ft.TextField(hint_text="Total a Pagar $0", border="none", text_size=90, width=page.width-50, text_align="right", read_only=True)
    total=ft.TextField(hint_text="Total $0", border="none", text_size=65, width=600, text_align="left", read_only=True)
    # total.hint_text = "Total $" + "999,999,999"

    card=ft.Card(
        margin=ft.margin.only(0, 50, 0, 0),
        offset=ft.transform.Offset(2,0),
        animate_offset=ft.animation.Animation(300, curve="easeIn"),
        elevation=30,
        content=ft.Container(
            ft.Column([
                ft.Row([
                    # ft.Text("Registro", size=20, weight="bold"),
                    ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                    ft.IconButton(
                        icon="close",
                        icon_size=30,
                        on_click=hideInputs
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row([
                    ft.Column([
                        rdbVehiculo,
                        placa,
                        total
                    ])
                ],
                alignment=ft.MainAxisAlignment.CENTER
                # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                # spacing=20
                ),
                ft.Row([
                    # tblRegistro
                    lv
                ],
                height=268,
                alignment=ft.MainAxisAlignment.CENTER,
                
                # spacing=20
                ),
                # ft.Row([
                #     ft.Column([
                #     ft.Text("", size=20, width=530),
                #     ]),
                #     ft.Column([
                #         placa
                #     ]),
                # ],
                # alignment=ft.MainAxisAlignment.END
                # ),
                # ft.Row([
                #     total
                # ],
                # alignment=ft.MainAxisAlignment.END
                # ),
            ]),
            padding=ft.padding.all(10)
        )
    )

    container=ft.Container(
        ft.Column([
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Image(
                        src=f"img/fondo.jpg",
                        # width=300,
                        # height=300,
                        fit=ft.ImageFit.COVER
                    ),
                    # ft.Row([
                        ft.ElevatedButton("Registro", on_click=showInputs),
                        # tblRegistro
                        card
                    # ]),
                    # card
                ]),
            )
        ])
    )

    page.window_always_on_top=True
    page.window_maximizable=False
    page.window_resizable=False
    # page.window_height=600
    # page.window_width=800
    # page.window_center()
    # page.window_bgcolor=ft.colors.TRANSPARENT
    page.window_opacity=0.8
    # page.bgcolor=ft.colors.TRANSPARENT
    page.opacity=0.0
    page.title="Parqueadero"
    # page.window_maximized=True
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.add(container)
    page.update()

    showInputs
    selectRegisters()
    tblRegistro.scroll="aito"
    tblRegistro.update()
    lv.update()

ft.app(target=main)
# ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9000)