import flet as ft
import settings

def Profile(page):
    photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    login_nombre=ft.Text(settings.login_nombre)
    btn_photo=ft.IconButton(icon=ft.icons.CAMERA_ALT, icon_size=35)

    return ft.Column([
        ft.Container(height=100),
        photo,
        btn_photo,
        login_nombre
    ],
    horizontal_alignment="center"
    )