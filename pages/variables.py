import flet as ft
from datatable import get_variables, update_variables
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

# class Variables(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#         self.variables=get_variables()

#         if self.variables != None:
#             self.id=self.variables[0][0]
#             self.valor_hora_moto=self.variables[0][1]
#             self.valor_dia_moto=self.variables[0][2]
#             self.valor_hora_carro=self.variables[0][3]
#             self.valor_dia_carro=self.variables[0][4]
#             self.valor_hora_otro=self.variables[0][5]
#             self.valor_dia_otro=self.variables[0][6]

#         def validateVariables(e):
#             self.vlr_hora_moto.error_text=""
#             self.vlr_dia_moto.error_text=""
#             self.vlr_hora_carro.error_text=""
#             self.vlr_dia_carro.error_text=""
#             self.vlr_hora_otro.error_text=""
#             self.vlr_dia_otro.error_text=""
#             if self.vlr_hora_moto.value == "":
#                 self.vlr_hora_moto.error_text="Campo requerido"
#                 # self.vlr_hora_moto.focus()
#                 self.btn_save.focus()
#                 self.vlr_hora_moto.update()
#             else:
#                 self.vlr_hora_moto.update()
#             if self.vlr_dia_moto.value == "":
#                 self.vlr_dia_moto.error_text="Campo requerido"
#                 # self.vlr_dia_moto.focus()
#                 self.vlr_dia_moto.update()
#             if self.vlr_hora_carro.value == "":
#                 self.vlr_hora_carro.error_text="Campo requerido"
#                 # self.vlr_hora_carro.focus()
#                 self.vlr_hora_carro.update()
#             if self.vlr_dia_carro.value == "":
#                 self.vlr_dia_carro.error_text="Campo requerido"
#                 # self.vlr_dia_carro.focus()
#                 self.vlr_dia_carro.update()
#             if self.vlr_hora_otro.value == "":
#                 self.vlr_hora_otro.error_text="Campo requerido"
#                 # self.vlr_hora_otro.focus()
#                 self.vlr_hora_otro.update()
#             if self.vlr_dia_otro.value == "":
#                 self.vlr_dia_otro.error_text="Campo requerido"
#                 # self.vlr_dia_otro.focus()
#                 self.vlr_dia_otro.update()
#             self.btn_save.focus()
#             if self.vlr_hora_moto.value != "" and self.vlr_dia_moto.value != "" and self.vlr_hora_carro.value != "" and self.vlr_dia_carro.value != "" and self.vlr_hora_otro.value != "" and self.vlr_dia_otro.value != "":
#                 self.vlr_hora_moto.update()
#                 self.vlr_dia_moto.update()
#                 self.vlr_hora_carro.update()
#                 self.vlr_dia_carro.update()
#                 self.vlr_hora_otro.update()
#                 self.vlr_dia_otro.update()
#                 update_variables(self.vlr_hora_moto.value, self.vlr_dia_moto.value, self.vlr_hora_carro.value, self.vlr_dia_carro.value, self.vlr_hora_otro.value, self.vlr_dia_otro.value, self.variable_id)

#         self.variable_id=self.id
#         self.vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_hora_moto)
#         self.vlr_dia_moto=ft.TextField(label="Día Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_dia_moto)
#         self.vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_hora_carro)
#         self.vlr_dia_carro=ft.TextField(label="Día Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_dia_carro)
#         self.vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_hora_otro)
#         self.vlr_dia_otro=ft.TextField(label="Día Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_dia_otro)
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
#                             self.vlr_dia_moto,
#                             self.vlr_hora_carro,
#                             self.vlr_dia_carro,
#                             self.vlr_hora_otro,
#                             self.vlr_dia_otro,
#                             self.btn_save
#                         ])
#                     ], 
#                     alignment=ft.MainAxisAlignment.CENTER,
#                     ),
#                 ),
#             ]
#         )

def Variables(page):
    variables=get_variables()

    if variables != None:
        id=variables[0][0]
        valor_hora_moto=variables[0][1]
        valor_dia_moto=variables[0][2]
        valor_hora_carro=variables[0][3]
        valor_dia_carro=variables[0][4]
        valor_hora_otro=variables[0][5]
        valor_dia_otro=variables[0][6]

    def validateVariables(e):
        vlr_hora_moto.error_text=""
        vlr_dia_moto.error_text=""
        vlr_hora_carro.error_text=""
        vlr_dia_carro.error_text=""
        vlr_hora_otro.error_text=""
        vlr_dia_otro.error_text=""
        if vlr_hora_moto.value == "":
            vlr_hora_moto.error_text="Campo requerido"
            # vlr_hora_moto.focus()
            btn_save.focus()
            vlr_hora_moto.update()
        else:
            vlr_hora_moto.update()
        if vlr_dia_moto.value == "":
            vlr_dia_moto.error_text="Campo requerido"
            # vlr_dia_moto.focus()
            vlr_dia_moto.update()
        if vlr_hora_carro.value == "":
            vlr_hora_carro.error_text="Campo requerido"
            # vlr_hora_carro.focus()
            vlr_hora_carro.update()
        if vlr_dia_carro.value == "":
            vlr_dia_carro.error_text="Campo requerido"
            # vlr_dia_carro.focus()
            vlr_dia_carro.update()
        if vlr_hora_otro.value == "":
            vlr_hora_otro.error_text="Campo requerido"
            # vlr_hora_otro.focus()
            vlr_hora_otro.update()
        if vlr_dia_otro.value == "":
            vlr_dia_otro.error_text="Campo requerido"
            # vlr_dia_otro.focus()
            vlr_dia_otro.update()
        btn_save.focus()
        if vlr_hora_moto.value != "" and vlr_dia_moto.value != "" and vlr_hora_carro.value != "" and vlr_dia_carro.value != "" and vlr_hora_otro.value != "" and vlr_dia_otro.value != "":
            vlr_hora_moto.update()
            vlr_dia_moto.update()
            vlr_hora_carro.update()
            vlr_dia_carro.update()
            vlr_hora_otro.update()
            vlr_dia_otro.update()
            update_variables(vlr_hora_moto.value, vlr_dia_moto.value, vlr_hora_carro.value, vlr_dia_carro.value, vlr_hora_otro.value, vlr_dia_otro.value, variable_id)

    variable_id=id
    vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_hora_moto)
    vlr_dia_moto=ft.TextField(label="Día Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_dia_moto)
    vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_hora_carro)
    vlr_dia_carro=ft.TextField(label="Día Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_dia_carro)
    vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=valor_hora_otro)
    vlr_dia_otro=ft.TextField(label="Día Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=valor_dia_otro)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateVariables)

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
                        vlr_hora_moto,
                        vlr_dia_moto,
                        vlr_hora_carro,
                        vlr_dia_carro,
                        vlr_hora_otro,
                        vlr_dia_otro,
                        btn_save
                    ])
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
        ]
    )