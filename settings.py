import flet as ft

global username, acceso_configuracion, acceso_variables, acceso_registro, acceso_cuadre, acceso_cierre, textsize, fieldwith, sw

username=""
login_nombre=""
message=""
acceso_configuracion=0
acceso_variables=0
acceso_registro=0
acceso_cuadre=0
acceso_cierre=0
textsize=30
fieldwith=280
sw=0 # sw=0 Escritorio sw=1 Web
page:ft.Page

def showMessage(bgcolor):
    page.snack_bar=ft.SnackBar(
        ft.Text(message, text_align="center"),
        bgcolor=bgcolor
    )
    page.snack_bar.open=True
    page.update()