import flet as ft
from datatable import get_configuration, update_configuration
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

class Configuration(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

        self.configuracion=get_configuration()

        if self.configuracion != None:
            self.id=self.configuracion[0][0]
            self.parqueadero=self.configuracion[0][1]
            self.nit=self.configuracion[0][2]
            self.regimen=self.configuracion[0][3]
            self.direccion=self.configuracion[0][4]
            self.telefono=self.configuracion[0][5]
            self.servicio=self.configuracion[0][6]
            self.consecutivo=self.configuracion[0][7]

        def validateConfiguration(e):
            self.parqueadero.error_text=""
            self.nit.error_text=""
            self.regimen.error_text=""
            self.direccion.error_text=""
            self.telefono.error_text=""
            self.servicio.error_text=""
            self.consecutivo.error_text=""
            if self.parqueadero.value == "":
                self.parqueadero.error_text="Campo requerido"
                self.btn_save.focus()
                self.parqueadero.update()
            else:
                self.parqueadero.update()
            if self.nit.value == "":
                self.nit.error_text="Campo requerido"
                self.nit.update()
            else:
                self.nit.update()
            if self.regimen.value == "":
                self.regimen.error_text="Campo requerido"
                self.regimen.update()
            else:
                self.regimen.update()
            if self.direccion.value == "":
                self.direccion.error_text="Campo requerido"
                self.direccion.update()
            else:
                self.direccion.update()
            if self.telefono.value == "":
                self.telefono.error_text="Campo requerido"
                self.telefono.update()
            else:
                self.telefono.update()
            if self.servicio.value == "":
                self.servicio.error_text="Campo requerido"
                self.servicio.update()
            else:
                self.servicio.update()
            if self.consecutivo.value == "":
                self.consecutivo.error_text="Campo requerido"
                self.consecutivo.update()
            else:
                self.consecutivo.update()
            self.btn_save.focus()
            if self.parqueadero.value != "" and self.nit.value != "" and self.regimen.value != "" and self.direccion.value != "" and self.telefono.value != "" and self.servicio.value != "" and self.consecutivo.value != "":
                self.parqueadero.update()
                self.nit.update()
                self.regimen.update()
                self.direccion.update()
                self.telefono.update()
                self.servicio.update()
                self.consecutivo.update()
                update_configuration(self.parqueadero.value, self.nit.value, self.regimen.value, self.direccion.value, self.telefono.value, self.servicio.value, self.consecutivo.value, self.configuracion_id)

        self.configuracion_id=self.id
        self.parqueadero=ft.TextField(label="Parqueadero", width=280, value=self.parqueadero)
        self.nit=ft.TextField(label="Nit", width=280, value=self.nit)
        self.regimen=ft.TextField(label="Regimen", width=280, value=self.regimen)
        self.direccion=ft.TextField(label="Dirección", width=280, value=self.direccion)
        self.telefono=ft.TextField(label="Teléfono", width=280, value=self.telefono)
        self.servicio=ft.TextField(label="Servicio", width=280, value=self.servicio)
        self.consecutivo=ft.TextField(label="Consecutivo", width=280, value=self.consecutivo)
        self.btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=validateConfiguration)

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(height=20),
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Stack([
                        ft.Row([
                            ft.Column([
                                ft.Text("Configuración", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
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
                            self.parqueadero,
                            self.nit,
                            self.regimen,
                            self.direccion,
                            self.telefono,
                            self.servicio,
                            self.consecutivo,
                            self.btn_save
                        ])
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            ]
        )