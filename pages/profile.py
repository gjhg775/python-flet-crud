import os
import shutil
import flet as ft
import settings
from datatable import selectUser, update_user, get_user
from pathlib import Path

def Profile(page):

    def save_upload(e:ft.FilePickerResultEvent):
        if e.files != None:
            for x in e.files:
                username=settings.username
                get_user(username)
                if settings.photo != "default.jpg":
                    os.remove(os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
                # settings.photo=settings.username.lower() + Path(x.name).suffix
                settings.photo=x.name
                # path=os.path.join(os.getcwd(), "upload\\img\\" + photo)
                shutil.copy(x.path, os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
                # # settings.avatar.src=path
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                # settings.user_photo.src=f"upload\\img\\{photo}"
                # settings.user_photo.update()
                # settings.page.update()
                update_user(username, settings.password, settings.photo)
                get_user(username)
                # photo=settings.photo
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                if settings.tipo_app == 0:
                    settings.user_avatar.src=f"upload\\img\\{settings.photo}"
                    settings.user_photo.src=f"upload\\img\\{settings.photo}"
                else:
                    settings.user_avatar.src=f"img/{settings.photo}"
                    settings.user_photo.src=f"img/{settings.photo}"
                settings.user_avatar.update()
                settings.user_photo.update()
                # settings.page.update()

    username=settings.username

    def changePassword(e):
        current_password.error_text=""
        password.error_text=""
        confirm_password.error_text=""
        if current_password.value != "" and password.value != "" and confirm_password.value != "":
            login_user, correo_electronico, login_password, login_nombre, login_photo, bln_login=selectUser(settings.username, current_password.value)
            if login_nombre != "":
                update_user(settings.username, password.value, settings.photo)
                current_password.disabled=False
                current_password.value=""
                password.value=""
                confirm_password.value=""
                settings.token_password=""
                settings.page.update()
        else:
            if current_password.value == "":
                current_password.error_text="Digite la contraseña actual"
                btn_save.focus()
            if password.value == "":
                password.error_text="Digite la contraseña nueva"
                btn_save.focus()
            if confirm_password.value == "":
                confirm_password.error_text="Confirme la contraseña"
                btn_save.focus()
            current_password.update()
            password.update()
            confirm_password.update()

    get_user(username)
    # photo=settings.photo
    # settings.user_avatar.src=f"upload\\img\\{settings.photo}"
    # settings.user_photo.src=f"upload\\img\\{settings.photo}"
    # settings.user_photo=ft.Image(src=f"upload\\img\\{settings.photo}" if settings.photo != "default.jpg" else f"img/{settings.photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_avatar.update()
    # settings.user_photo.update()
    # settings.page.update()

    # user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    
    file_picker=ft.FilePicker(on_result=save_upload)

    # photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    login_nombre=ft.Text(settings.login_nombre, theme_style=ft.TextThemeStyle.TITLE_LARGE)
    # photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    if settings.tipo_app == 0:
    #     # settings.avatar=ft.Image(src=os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}") if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
        settings.user_photo=ft.Image(src=f"upload\\img\\{settings.photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
        # user_avatar=ft.Image(src=f"upload\\img\\{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    else:
    #     # settings.avatar=ft.Image(src=f"img/{settings.photo}" if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    #     settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
        settings.user_photo=ft.Image(src=f"img/{settings.photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
        # user_avatar=ft.Image(src=f"img/{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    btn_photo=ft.IconButton(icon=ft.icons.CAMERA_ALT, icon_size=35, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]))
    change_password=ft.Text("Cambiar contraseña", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    current_password=ft.TextField(width=280, height=60, hint_text="Contraseña actual", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, value=settings.token_password if settings.token_password != "" else "", disabled=True if settings.token_password != "" else False)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña nueva", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    confirm_password=ft.TextField(width=280, height=60, hint_text="Confirmar contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, visible=True)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=changePassword)
    
    settings.page.overlay.append(file_picker)

    return ft.Column([
        ft.Container(height=100),
        ft.Container(
            ft.Stack([
                settings.user_photo,
                ft.Column([
                    ft.Container(
                        btn_photo
                    ),
                ],
                left=220,
                top=240,
                ),
            ]),
        ),
        ft.Container(
            ft.Row([
                login_nombre
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
        ),
        ft.Container(height=20),
        ft.Container(
            ft.Column([
                change_password,
                current_password,
                password,
                confirm_password
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
        ),
        ft.Container(height=20),
            ft.Container(
                ft.Row([
                    btn_save
                ], 
                alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
            ft.Container(height=50),
    ],
    horizontal_alignment="center"
    )