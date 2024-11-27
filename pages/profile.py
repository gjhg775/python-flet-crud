import os
import sys
import flet as ft
import settings
import shutil
from datatable import selectUser, update_user, get_user
from pathlib import Path

def Profile(page):

    if getattr(sys, 'frozen', False):
        # Si está corriendo como un ejecutable
        base_path = sys._MEIPASS
    else:
        # Si está corriendo como un script en desarrollo
        base_path = os.path.abspath(".")

    # Para acceder a los archivos en assets o upload:
    assets_path = os.path.join(base_path, "assets")
    # upload_path = os.path.join(base_path, "upload")
    
    # Ejemplo de uso:
    # icon_path = os.path.join(assets_path, "img", "parqueadero.png")

    def save_upload(e:ft.FilePickerResultEvent):
        if e.files != None:
            for x in e.files:
                username=settings.username
                get_user(username)
                if settings.photo != "default.jpg" and settings.photo != "default1.jpg" and settings.photo != x.name:
                    # if settings.tipo_app == 0:
                    #     # os.remove(os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
                    #     os.remove(os.path.join(os.getcwd(), f"\\img\\{settings.photo}"))
                    # else:
                    #     os.remove(os.path.join(os.getcwd(), f"img/{settings.photo}"))
                    # os.remove(os.path.join(os.getcwd(), f"upload/img/{settings.photo}"))
                    os.remove(os.path.join(assets_path, "img", f"{settings.photo}"))
                # settings.photo=settings.username.lower() + Path(x.name).suffix
                settings.photo=x.name
                # path=os.path.join(os.getcwd(), "upload\\img\\" + photo)
                # if settings.tipo_app == 0:
                #     # shutil.copy(x.path, os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}"))
                #     shutil.copy(x.path, os.path.join(os.getcwd(), f"\\img\\{settings.photo}"))
                # else:
                #     shutil.copy(x.path, os.path.join(os.getcwd(), f"img/{settings.photo}"))
                if settings.photo != "default.jpg" and settings.photo != "default1.jpg":
                    shutil.copy(x.path, os.path.join(assets_path, "img", f"{settings.photo}"))
                # # settings.avatar.src=path
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                # settings.user_photo.src=f"upload\\img\\{photo}"
                # settings.user_photo.update()
                # settings.page.update()
                update_user(username, settings.correo_electronico, settings.password, settings.photo, "photo")
                get_user(username)
                # photo=settings.photo
                # settings.user_avatar.src=f"upload\\img\\{photo}"
                # settings.user_avatar.src=os.path.join(assets_path, "img", f"{settings.photo}")
                # settings.user_photo.src=os.path.join(assets_path, "img", f"{settings.photo}")
                settings.user_avatar.src=f"/img/{settings.photo}"
                settings.user_photo.src=f"/img/{settings.photo}"
                # if settings.tipo_app == 0:
                #     settings.user_avatar.src=f"assets\\img\\{settings.photo}"
                #     settings.user_photo.src=f"assets\\img\\{settings.photo}"
                # else:
                #     settings.user_avatar.src=f"img/{settings.photo}"
                #     settings.user_photo.src=f"img/{settings.photo}"
                settings.user_avatar.update()
                settings.user_photo.update()
                # settings.page.update()

    username=settings.username

    def changeEmail(e):
        correo.error_text=""
        if correo.value != "":
            settings.correo_electronico=correo.value
            update_user(settings.username, settings.correo_electronico, settings.password, settings.photo, "update")
            settings.page.update()
        else:
            correo.error_text="Digite el correo electrónico"
            btn_save_email.focus()
            settings.page.update()

    def changePassword(e):
        current_password.error_text=""
        password.error_text=""
        confirm_password.error_text=""
        if current_password.value != "" and password.value != "" and confirm_password.value != "":
            login_user, correo_electronico, login_password, login_nombre, login_photo, bln_login=selectUser(settings.username, current_password.value)
            if login_nombre != "":
                update_user(settings.username, password.value, settings.photo, "save")
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
    correo=ft.TextField(width=280, height=60, hint_text="Correo electrónico", border="underline", prefix_icon=ft.icons.EMAIL, text_align="left", value=settings.correo_electronico)
    btn_save_email=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=changeEmail)
    # photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    settings.user_photo=ft.Image(src=f"/img/{settings.photo}", height=200, width=200, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_photo=ft.Image(src=f"{assets_path}/img/{settings.photo}", height=200, width=200, fit=ft.ImageFit.COVER, border_radius=150)
    # if settings.tipo_app == 0:
    # #     # settings.avatar=ft.Image(src=os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}") if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    #     settings.user_photo=ft.Image(src=f"upload\\img\\{settings.photo}", height=200, width=200, fit=ft.ImageFit.COVER, border_radius=150)
    #     # user_avatar=ft.Image(src=f"upload\\img\\{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    # else:
    # #     # settings.avatar=ft.Image(src=f"img/{settings.photo}" if settings.photo != "" else f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    # #     settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    #     settings.user_photo=ft.Image(src=f"img/{settings.photo}", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    #     # user_avatar=ft.Image(src=f"img/{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    btn_photo=ft.IconButton(icon=ft.icons.CAMERA_ALT, icon_size=35, on_click=lambda _: file_picker.pick_files(allow_multiple=False, allowed_extensions=["jpg", "jpeg", "png"]))
    change_password=ft.Text("Cambiar contraseña", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, text_align="left", color=ft.colors.PRIMARY)
    current_password=ft.TextField(width=280, height=60, hint_text="Contraseña actual", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, value=settings.token_password if settings.token_password != "" else "", disabled=True if settings.token_password != "" else False)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña nueva", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    confirm_password=ft.TextField(width=280, height=60, hint_text="Confirmar contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, visible=True)
    btn_save=ft.ElevatedButton("Guardar", icon=ft.icons.SAVE_SHARP, width=280, bgcolor=ft.colors.BLUE_900, color="white", autofocus=True, on_click=changePassword)
    
    settings.page.overlay.append(file_picker)

    # if settings.tipo_app == 0:
    body=ft.Column([
        ft.Container(height=10),
        ft.Container(
            ft.Stack([
                settings.user_photo,
                ft.Column([
                    ft.Container(
                        btn_photo
                    ),
                ],
                left=150,
                top=150,
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
        ft.Container(height=10),
        ft.Container(
            ft.Row([
                correo
            ],
            alignment=ft.MainAxisAlignment.CENTER
            ),
        ),
        ft.Container(
            ft.Row([
                btn_save_email
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            ),
        ),
        ft.Container(height=10),
        ft.Container(height=10),
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
        ft.Container(height=10),
        ft.Container(
            ft.Row([
                btn_save
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            ),
        ),
        ft.Container(height=10),
    ],
    horizontal_alignment="center"
    )
    # else:
    #     btn_home=ft.FilledButton("Inicio".ljust(21, " "), icon=ft.icons.HOME, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/"))
    #     btn_users=ft.FilledButton("Usuarios".ljust(18, " "), icon=ft.icons.PERSON_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/users"))
    #     btn_settings=ft.FilledButton("Configuración", icon=ft.icons.SETTINGS, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/configuration"))
    #     btn_variables=ft.FilledButton("Variables".ljust(18, " "), icon=ft.icons.FACT_CHECK, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/variables"))
    #     btn_register=ft.FilledButton("Registro".ljust(18, " "), icon=ft.icons.EDIT_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/register"))
    #     btn_cash_register=ft.FilledButton("Cuadre de caja", icon=ft.icons.ATTACH_MONEY_SHARP, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/cash_register"))
    #     btn_closing_day=ft.FilledButton("Cierre de día".ljust(18, " "), icon=ft.icons.CALENDAR_MONTH, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/closing_day"))
    #     btn_developer=ft.FilledButton("Desarrollador".ljust(16, " "), icon=ft.icons.CODE_ROUNDED, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/developer"))
    #     btn_logout=ft.FilledButton("Cerrar sesión".ljust(16, " "), icon=ft.icons.POWER_SETTINGS_NEW, icon_color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, style=ft.ButtonStyle(color={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_900,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.WHITE,
    #             }, bgcolor={
    #                 ft.ControlState.HOVERED: ft.colors.BLUE_50,
    #                 ft.ControlState.FOCUSED: ft.colors.BLUE,
    #                 ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
    #             }), on_click=lambda _: page.go("/login"))
        
    #     body=ft.Column(
    #         controls=[
    #             ft.Row([
    #                 ft.Container(
    #                     height=938,
    #                     width=200,
    #                     shadow=ft.BoxShadow(
    #                         spread_radius=1,
    #                         blur_radius=15,
    #                         color=ft.colors.BLUE_GREY_300,
    #                         offset=ft.Offset(0, 0),
    #                         blur_style=ft.ShadowBlurStyle.OUTER,
    #                     ),
    #                     # expand=2,
    #                     padding=ft.padding.only(0, 20, 0, 0),
    #                     bgcolor=ft.colors.BLUE_900,
    #                     border_radius=ft.border_radius.all(10),
    #                     # alignment=ft.alignment.center,
    #                     content=ft.Column([
    #                         # btn_profile,
    #                         ft.Container(
    #                             padding=ft.padding.only(10, 10, 10, 10),
    #                             on_click=lambda e: settings.page.go("/profile"),
    #                             content=ft.Row([
    #                                 settings.user_avatar,
    #                                 # settings.page.user_auth
    #                             ]),
    #                         ),
    #                         ft.Divider(thickness=2),
    #                         btn_home,
    #                         btn_users,
    #                         btn_settings,
    #                         btn_variables,
    #                         btn_register,
    #                         btn_cash_register,
    #                         btn_closing_day,
    #                         ft.Divider(thickness=2),
    #                         btn_developer,
    #                         ft.Divider(thickness=2),
    #                         btn_logout
    #                     ],
    #                     horizontal_alignment="center",
    #                     ),
    #                 ),
    #                 ft.Container(
    #                     expand=10,
    #                     padding=ft.padding.only(0, 20, 0, 0),
    #                     # bgcolor="blue",
    #                     content=ft.Column([
    #                         ft.Container(height=10),
    #                         ft.Container(
    #                             ft.Stack([
    #                                 settings.user_photo,
    #                                 ft.Column([
    #                                     ft.Container(
    #                                         btn_photo
    #                                     ),
    #                                 ],
    #                                 left=220,
    #                                 top=240,
    #                                 ),
    #                             ]),
    #                         ),
    #                         ft.Container(
    #                             ft.Row([
    #                                 login_nombre
    #                             ],
    #                             alignment=ft.MainAxisAlignment.CENTER
    #                             ),
    #                         ),
    #                         ft.Container(height=10),
    #                         ft.Container(
    #                             ft.Column([
    #                                 change_password,
    #                                 current_password,
    #                                 password,
    #                                 confirm_password
    #                             ],
    #                             alignment=ft.MainAxisAlignment.CENTER
    #                             ),
    #                         ),
    #                         ft.Container(height=10),
    #                             ft.Container(
    #                                 ft.Row([
    #                                     btn_save
    #                                 ], 
    #                                 alignment=ft.MainAxisAlignment.CENTER,
    #                                 ),
    #                             ),
    #                             ft.Container(height=50),
    #                     ],
    #                     horizontal_alignment="center"
    #                     )
    #                 )
    #             ]),
    #         ]
    #     )

    return body