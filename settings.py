import flet as ft

global username, correo_electronico, password, token_password, photo, user_avatar, user_photo, usuario, acceso_usuarios, acceso_configuracion, acceso_variables, acceso_registro, \
       acceso_cuadre, acceso_cierre, textsize, fieldwith, tipo_app, preview_register, print_register_receipt, valor_duplicado, send_email_register, preview_cash, print_cash_receipt, \
       printer, paper_width, resolucion, fecha_desde, fecha_hasta, prefijo, autoriza_del, autoriza_al, billing, clave_tecnica, tipo_ambiente, cliente_final, consecutivo, consecutivo2, \
       placa, progressRing, correcto, errors, acceso, user_auth, email_user, email_pass, secret_key, parqueadero

username=""
correo_electronico=""
password=""
token_password=""
login_nombre=""
photo=""
message=""
usuario=""
printer=""
resolucion=""
fecha_desde=""
fecha_hasta=""
prefijo=""
autoriza_del=""
autoriza_al=""
clave_tecnica=""
cliente_final=""
consecutivo=""
consecutivo2=""
placa=""
user_auth=""
email_user=""
email_pass=""
secret_key=""
parqueadero=""
acceso_usuarios=0
acceso_configuracion=0
acceso_variables=0
acceso_registro=0
acceso_cuadre=0
acceso_cierre=0
acceso=1
textsize=30
fieldwith=800
tipo_app=0 # 0=Escritorio 1=Web
billing=1
tipo_ambiente=0
paper_width=0
preview_register=1
print_register_receipt=1
valor_duplicado=0
send_email_register=0
preview_cash=1
print_cash_receipt=1
correcto=0
errors=0
page=ft.Page
progressRing=ft.ProgressRing()
progressBar=ft.ProgressBar(width=page.width, color="amber", bgcolor="#eeeeee", visible=False)

# if sw == 0:
#     user_avatar=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"upload\\img\\{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
# else:
#     user_avatar=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"img/{photo}" if photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

user_avatar=ft.Image(src=f"/img/{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
user_photo=ft.Image(src=f"/img/{photo}", height=200, width=200, fit=ft.ImageFit.COVER, border_radius=150)

label_0=ft.Text()

# if tipo_app == 0:
#     user_avatar=ft.Image(src=f"img\\{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"img\\{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
# else:
#     user_avatar=ft.Image(src=f"img/{photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
#     user_photo=ft.Image(src=f"img/{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

def showMessage(bgcolor):
    snack_bar=ft.SnackBar(
        ft.Text(message, text_align="center"),
        bgcolor=bgcolor,
        duration=2000,
        open=True
    )
    # if tipo_app == 0:
    page.overlay.append(snack_bar)
    # page.snack_bar.open=True
    page.update()

def close_banner(e):
    page.close(banner)

def show_banner():
    page.open(banner)

action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
banner = ft.Banner(
    bgcolor=ft.colors.AMBER_100,
    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
    content=ft.Text(
        value="",
        color=ft.colors.BLACK,
    ),
    actions=[
        ft.TextButton(text="Cerrar", style=action_button_style, on_click=close_banner),
    ],
)

# def close_dlg(e):
#     dlg_modal.open=False
#     page.update()

# def open_dlg_modal_email():
#     dlg_modal.title=ft.Text("Correo electrónico", text_align="center")
#     dlg_modal.content=ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL, text_align="left", value=correo_electronico)
#     dlg_modal.open=True
#     page.overlay.append(dlg_modal)
#     page.update()

# dlg_modal=ft.AlertDialog(
#     bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
#     modal=True,
#     # icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
#     # title=ft.Text(title, text_align="center"),
#     # content=ft.Text(message, text_align="center"),
#     actions=[
#         ft.TextButton("Enviar", autofocus=True, on_click=close_dlg)
#     ],
#     actions_alignment=ft.MainAxisAlignment.END,
#     # on_dismiss=lambda _: date_button.focus(),
# )