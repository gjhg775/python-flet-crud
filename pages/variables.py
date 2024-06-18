import flet as ft
import settings
import sqlite3
from datatable import get_variables, update_variables

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)
message=""

# class Variables(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#         self.variables=get_variables()

#         if self.variables != None:
#             self.id=self.variables[0][0]
#             self.valor_hora_moto=self.variables[0][1]
#             self.valor_turno_moto=self.variables[0][2]
#             self.valor_hora_carro=self.variables[0][3]
#             self.valor_turno_carro=self.variables[0][4]
#             self.valor_hora_otro=self.variables[0][5]
#             self.valor_turno_otro=self.variables[0][6]

#         def validateVariables(e):
#             self.vlr_hora_moto.error_text=""
#             self.vlr_turno_moto.error_text=""
#             self.vlr_hora_carro.error_text=""
#             self.vlr_turno_carro.error_text=""
#             self.vlr_hora_otro.error_text=""
#             self.vlr_turno_otro.error_text=""
#             if self.vlr_hora_moto.value == "":
#                 self.vlr_hora_moto.error_text="Campo requerido"
#                 # self.vlr_hora_moto.focus()
#                 self.btn_save.focus()
#                 self.vlr_hora_moto.update()
#             else:
#                 self.vlr_hora_moto.update()
#             if self.vlr_turno_moto.value == "":
#                 self.vlr_turno_moto.error_text="Campo requerido"
#                 # self.vlr_turno_moto.focus()
#                 self.vlr_turno_moto.update()
#             if self.vlr_hora_carro.value == "":
#                 self.vlr_hora_carro.error_text="Campo requerido"
#                 # self.vlr_hora_carro.focus()
#                 self.vlr_hora_carro.update()
#             if self.vlr_turno_carro.value == "":
#                 self.vlr_turno_carro.error_text="Campo requerido"
#                 # self.vlr_turno_carro.focus()
#                 self.vlr_turno_carro.update()
#             if self.vlr_hora_otro.value == "":
#                 self.vlr_hora_otro.error_text="Campo requerido"
#                 # self.vlr_hora_otro.focus()
#                 self.vlr_hora_otro.update()
#             if self.vlr_turno_otro.value == "":
#                 self.vlr_turno_otro.error_text="Campo requerido"
#                 # self.vlr_turno_otro.focus()
#                 self.vlr_turno_otro.update()
#             self.btn_save.focus()
#             if self.vlr_hora_moto.value != "" and self.vlr_turno_moto.value != "" and self.vlr_hora_carro.value != "" and self.vlr_turno_carro.value != "" and self.vlr_hora_otro.value != "" and self.vlr_turno_otro.value != "":
#                 self.vlr_hora_moto.update()
#                 self.vlr_turno_moto.update()
#                 self.vlr_hora_carro.update()
#                 self.vlr_turno_carro.update()
#                 self.vlr_hora_otro.update()
#                 self.vlr_turno_otro.update()
#                 update_variables(self.vlr_hora_moto.value, self.vlr_turno_moto.value, self.vlr_hora_carro.value, self.vlr_turno_carro.value, self.vlr_hora_otro.value, self.vlr_turno_otro.value, self.variable_id)

#         self.variable_id=self.id
#         self.vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_hora_moto)
#         self.vlr_turno_moto=ft.TextField(label="Turno Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=self.valor_turno_moto)
#         self.vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_hora_carro)
#         self.vlr_turno_carro=ft.TextField(label="Turno Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=self.valor_turno_carro)
#         self.vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_hora_otro)
#         self.vlr_turno_otro=ft.TextField(label="Turno Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=self.valor_turno_otro)
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
#                             self.vlr_turno_moto,
#                             self.vlr_hora_carro,
#                             self.vlr_turno_carro,
#                             self.vlr_hora_otro,
#                             self.vlr_turno_otro,
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
        valor_turno_moto=variables[0][2]
        valor_hora_carro=variables[0][3]
        valor_turno_carro=variables[0][4]
        valor_hora_otro=variables[0][5]
        valor_turno_otro=variables[0][6]

    def validateVariables(e):
        vlr_hora_moto.error_text=""
        vlr_turno_moto.error_text=""
        vlr_hora_carro.error_text=""
        vlr_turno_carro.error_text=""
        vlr_hora_otro.error_text=""
        vlr_turno_otro.error_text=""
        if vlr_hora_moto.value == "":
            vlr_hora_moto.error_text="Campo requerido"
            # vlr_hora_moto.focus()
            btn_save.focus()
            vlr_hora_moto.update()
        else:
            vlr_hora_moto.update()
        if vlr_turno_moto.value == "":
            vlr_turno_moto.error_text="Campo requerido"
            # vlr_turno_moto.focus()
            vlr_turno_moto.update()
        if vlr_hora_carro.value == "":
            vlr_hora_carro.error_text="Campo requerido"
            # vlr_hora_carro.focus()
            vlr_hora_carro.update()
        if vlr_turno_carro.value == "":
            vlr_turno_carro.error_text="Campo requerido"
            # vlr_turno_carro.focus()
            vlr_turno_carro.update()
        if vlr_hora_otro.value == "":
            vlr_hora_otro.error_text="Campo requerido"
            # vlr_hora_otro.focus()
            vlr_hora_otro.update()
        if vlr_turno_otro.value == "":
            vlr_turno_otro.error_text="Campo requerido"
            # vlr_turno_otro.focus()
            vlr_turno_otro.update()
        btn_save.focus()
        if vlr_hora_moto.value != "" and vlr_turno_moto.value != "" and vlr_hora_carro.value != "" and vlr_turno_carro.value != "" and vlr_hora_otro.value != "" and vlr_turno_otro.value != "":
            vlr_hora_moto.update()
            vlr_turno_moto.update()
            vlr_hora_carro.update()
            vlr_turno_carro.update()
            vlr_hora_otro.update()
            vlr_turno_otro.update()
            message=update_variables(vlr_hora_moto.value, vlr_turno_moto.value, vlr_hora_carro.value, vlr_turno_carro.value, vlr_hora_otro.value, vlr_turno_otro.value, variable_id)
            if message != "":
                bgcolor="green"
                settings.message=message
                settings.showMessage(bgcolor)

    variable_id=id
    vlr_hora_moto=ft.TextField(label="Hora Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_hora_moto)
    vlr_turno_moto=ft.TextField(label="Turno Moto", width=280, prefix_icon=ft.icons.MOTORCYCLE_SHARP, value=valor_turno_moto)
    vlr_hora_carro=ft.TextField(label="Hora Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_hora_carro)
    vlr_turno_carro=ft.TextField(label="Turno Carro", width=280, prefix_icon=ft.icons.DIRECTIONS_CAR_SHARP, value=valor_turno_carro)
    vlr_hora_otro=ft.TextField(label="Hora Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=valor_hora_otro)
    vlr_turno_otro=ft.TextField(label="Turno Otro", width=280, prefix_icon=ft.icons.VIEW_LIST, value=valor_turno_otro)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateVariables)

    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Text("Variables", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
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
                        vlr_turno_moto,
                        vlr_hora_carro,
                        vlr_turno_carro,
                        vlr_hora_otro,
                        vlr_turno_otro,
                        btn_save
                    ])
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
        ]
    )