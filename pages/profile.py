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
                photo=settings.username.lower() + Path(x.name).suffix
                # settings.photo=photo
                # path=os.path.join(os.getcwd(), "upload\\img\\" + photo)
                shutil.copy(x.path, os.path.join(os.getcwd(), f"upload\\img\\{photo}"))
                # # settings.avatar.src=path
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                # settings.user_photo.src=f"upload\\img\\{photo}"
                # settings.user_photo.update()
                # settings.page.update()
                username=settings.username
                update_user(username, photo)
                photo=get_user(username)
                # photo=settings.photo
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                user_photo.src=f"upload\\img\\{photo}"
                user_photo.update()
                settings.page.update()

    username=settings.username
    photo=get_user(username)
    # photo=settings.photo
    # settings.user_avatar.src=f"upload\\img\\{photo}"
    # settings.user_photo.src=f"upload\\img\\{photo}"
    user_photo=ft.Image(src=f"upload\\img\\{photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # user_photo.update()
    settings.page.update()

    # user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    
    file_picker=ft.FilePicker(on_result=save_upload)

    # photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    login_nombre=ft.Text(settings.login_nombre, theme_style=ft.TextThemeStyle.TITLE_LARGE)
    # photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # if settings.sw == 0:
    #     # settings.avatar=ft.Image(src=os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}") if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # else:
    #     # settings.avatar=ft.Image(src=f"img/{settings.photo}" if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    #     settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    btn_photo=ft.IconButton(icon=ft.icons.CAMERA_ALT, icon_size=35, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]))
    
    settings.page.overlay.append(file_picker)

    return ft.Column([
        ft.Container(height=100),
        ft.Container(
            ft.Stack([
                user_photo,
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
    ],
    horizontal_alignment="center"
    )