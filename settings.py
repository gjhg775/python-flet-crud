import flet as ft

global username, photo, user_avatar, user_photo, usuario, acceso_configuracion, acceso_variables, acceso_registro, acceso_cuadre, acceso_cierre, textsize, fieldwith, sw, preview_register, print_register_receipt, preview_cash, print_cash_receipt, printer, progressRing

username=""
login_nombre=""
photo=""
message=""
usuario=""
printer=""
acceso_configuracion=0
acceso_variables=0
acceso_registro=0
acceso_cuadre=0
acceso_cierre=0
textsize=30
fieldwith=280
sw=0 # sw=0 Escritorio sw=1 Web
preview_register=1
print_register_receipt=1
preview_cash=1
print_cash_receipt=1
page:ft.Page
progressRing=ft.ProgressRing()

# if sw == 0:
#     user_avatar=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
# else:
#     user_avatar=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

if sw == 0:
    user_avatar=ft.Image(src=f"upload\\img\\{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    user_photo=ft.Image(src=f"upload\\img\\{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
else:
    user_avatar=ft.Image(src=f"img/{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    user_photo=ft.Image(src=f"img/{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

def showMessage(bgcolor):
    page.snack_bar=ft.SnackBar(
        ft.Text(message, text_align="center"),
        bgcolor=bgcolor,
        duration=2000
    )
    page.snack_bar.open=True
    page.update()