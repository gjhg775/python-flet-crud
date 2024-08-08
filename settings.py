import flet as ft

global username, photo, user_avatar, user_photo, usuario, acceso_configuracion, acceso_variables, acceso_registro, acceso_cuadre, acceso_cierre, textsize, fieldwith, tipo_app, \
       preview_register, print_register_receipt, preview_cash, print_cash_receipt, printer, paper_width, prefijo, billing, clave_tecnica, tipo_ambiente, cliente_final, \
       progressRing

username=""
login_nombre=""
photo=""
message=""
usuario=""
printer=""
prefijo=""
clave_tecnica=""
cliente_final=""
acceso_configuracion=0
acceso_variables=0
acceso_registro=0
acceso_cuadre=0
acceso_cierre=0
textsize=30
fieldwith=280
tipo_app=0 # 0=Escritorio 1=Web
billing=1
tipo_ambiente=0
paper_width=0
preview_register=1
print_register_receipt=1
preview_cash=1
print_cash_receipt=1
page=ft.Page
progressRing=ft.ProgressRing()
progressBar=ft.ProgressBar(width=page.width, color="amber", bgcolor="#eeeeee", visible=False)

# if sw == 0:
#     user_avatar=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
# else:
#     user_avatar=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

if tipo_app == 0:
    user_avatar=ft.Image(src=f"upload\\img\\{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    user_photo=ft.Image(src=f"upload\\img\\{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
else:
    user_avatar=ft.Image(src=f"img/{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    user_photo=ft.Image(src=f"img/{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

def showMessage(bgcolor):
    snack_bar=ft.SnackBar(
        ft.Text(message, text_align="center"),
        bgcolor=bgcolor,
        duration=2000,
        open=True
    )
    page.overlay.append(snack_bar)
    # page.snack_bar.open=True
    page.update()