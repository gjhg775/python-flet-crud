import flet as ft
from datatable import get_variables, update_variables
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

class Variables(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

        variables = get_variables()

        if variables != None:
            id=variables[0][0]
            valor_hora_moto=variables[0][1]
            valor_dia_moto=variables[0][2]
            valor_hora_carro=variables[0][3]
            valor_dia_carro=variables[0][4]
            valor_hora_otro=variables[0][5]
            valor_dia_otro=variables[0][6]

        self.variable_id=id
        self.vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, height=60, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_hora_moto)
        self.vlr_dia_moto=ft.TextField(label="Día Moto", width=280, height=60, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_dia_moto)
        self.vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, height=60, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_hora_carro)
        self.vlr_dia_carro=ft.TextField(label="Día Carro", width=280, height=60, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_dia_carro)
        self.vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, height=60, prefix_icon=ft.icons.VIEW_LIST, value=valor_hora_otro)
        self.vlr_dia_otro=ft.TextField(label="Día Otro", width=280, height=60, prefix_icon=ft.icons.VIEW_LIST, value=valor_dia_otro)
        self.btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=lambda _:update_variables(self.vlr_hora_moto.value, self.vlr_dia_moto.value, self.vlr_hora_carro.value, self.vlr_dia_carro.value, self.vlr_hora_otro.value, self.vlr_dia_otro.value, self.variable_id))

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Stack([
                        ft.Row([
                            ft.Column([
                                ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
                            ])
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]),
                ),
                ft.Container(height=10),
                ft.Container(
                    ft.Row([
                        ft.Column([
                            self.vlr_hora_moto,
                            self.vlr_dia_moto,
                            self.vlr_hora_carro,
                            self.vlr_dia_carro,
                            self.vlr_hora_otro,
                            self.vlr_dia_otro,
                            self.btn_save
                        ])
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            ]
        )