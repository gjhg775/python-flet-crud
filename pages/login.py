import os
import re
import time
import flet as ft
import settings
import hashlib
from flet import icons
# from views import views_handler
# from pages.login import Login
# from pages.profile import Profile
from pages.home import Home
# from pages.users import Users
# from pages.configuration import Configuration
# from pages.variables import Variables
# from pages.register import *
# from pages.cash_register import *
# from pages.closing_day import Closing_day
# from pages.developer import Developer
from datatable import get_configuration, selectUser, selectAccess, add_user, get_user, reset_password, update_user, lblAccesos, tba
from decouple import config
from mail import send_mail_user

# def validateUser(e):
#     if user.value != "" and password.value != "":
#         usuario=user.value
#         contrasena=password.value
#         selectUser(usuario, contrasena)
#         # page.go("/register")
#     else:
#         user.focus()

# user=ft.TextField(
#     width=280,
#     height=40,
#     hint_text="Usuario",
#     border="underline",
#     color="black",
#     prefix_icon=ft.icons.PERSON_SHARP
# )

# password=ft.TextField(
#     width=280,
#     height=40,
#     hint_text="Contraseña",
#     border="underline",
#     color="black",
#     prefix_icon=ft.icons.LOCK,
#     password=True
# )

def Login(page):
    settings.user_avatar=ft.Image(src=f"\\img\\{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    user_auth=ft.Text("")

    def loginMe(e):
        lbl_login.value="Iniciar sesión"
        user.hint_text="Usuario ó correo electrónico"
        btn_login.text="Iniciar sesión"
        btn_login.on_click=login
        email.visible=False
        confirm_password.visible=False
        name.visible=False
        lbl_cuenta.value="¿No tiene una cuenta?"
        btn_cuenta.visible=True
        btn_loginme.visible=False
        btn_reset_password.visible=True
        user.value=""
        password.value=""
        user.error_text=""
        password.error_text=""
        name.error_text=""
        settings.page.update()

    def login(e):
        user.error_text=""
        password.error_text=""
        email.visible=False
        bln_login=False
        if user.value != "" and password.value != "":
            usuario=user.value
            contrasena=str(password.value)
            try:
                login_user, correo_electronico, login_password, login_nombre, login_photo, bln_login=selectUser(usuario, contrasena)
                if login_user != "" and bln_login == False:
                    user.error_text=login_user
                    # user.focus()
                    btn_login.focus()
                    user.update()
                else:
                    user.error_text=""
                    user.update()
                if login_password != "" and bln_login == False:
                    password.error_text=login_password
                    # password.focus()
                    btn_login.focus()
                    password.update()
                else:
                    password.error_text=""
                    password.update()
                if bln_login == True:
                    datalogin={"logged":bln_login, "username":login_user}
                    settings.page.session.set("username", datalogin["username"])
                    settings.username=settings.page.session.get("username")
                    username=settings.username
                    settings.photo=login_photo
                    if correo_electronico == "":
                        open_dlg_modal_email(e)
                    settings.correo_electronico=correo_electronico
                    selectAccess(username)
                    # settings.page.clean()
                    settings.page.route="/"
                    settings.page.go("/")
                    # settings.page.update()
                    # settings.page.clean()
                    # settings.page.add(Home(page))
                    # page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
                    # settings.page.appbar.title=ft.Text("Parqueadero", color=ft.colors.WHITE)
                    # settings.page.update()
                    # if settings.tipo_app == 0:
                    #     settings.user_avatar.src=f"img\\{login_photo}"
                    #     settings.user_photo.src=f"img\\{login_photo}"
                    # else:
                    #     settings.user_avatar.src=f"img/{login_photo}"
                    #     settings.user_photo.src=f"img/{login_photo}"
                    settings.user_avatar.src=f"/img/{login_photo}"
                    settings.user_photo.src=f"/img/{login_photo}"
                    settings.login_nombre=login_nombre
                    # user_auth.value=settings.login_nombre
                    # user_auth.update()
                    settings.message=f"Bienvenido {login_nombre}"
                    bgcolor="blue"
                else:
                    settings.message="Acceso denegado"
                    bgcolor="red"
                settings.showMessage(bgcolor)
                settings.page.update()
            except Exception as e:
                user.value=""
                password.value=""
                settings.show_banner()
                bgcolor="red"
                message="No se puede abrir la base de datos"
                settings.message=message
                settings.showMessage(bgcolor)
                # print(e)
        else:
            if user.value == "":
                user.error_text="Digite usuario ó correo electrónico"
                btn_login.focus()
            if password.value == "":
                password.error_text="Digite la contraseña"
                btn_login.focus()
            user.update()
            password.update()

    def signUp(e):
        message=""
        user.error_text=""
        email.error_text=""
        password.error_text=""
        confirm_password.error_text=""
        name.error_text=""
        bln_login=False
        if user.value != "" and email.value != "" and password.value != "" and confirm_password.value != "" and name.value != "":
            usuario=user.value
            correo_electronico=email.value
            contrasena=password.value
            confirm_contrasena=confirm_password.value
            nombre=name.value
            hash=hashlib.sha256(contrasena.encode()).hexdigest()
            hash2=hashlib.sha256(confirm_contrasena.encode()).hexdigest()
            if hash == hash2:
                sw=0
                foto="default.jpg"
                bln_login=add_user(usuario, correo_electronico, hash, nombre, foto)
                if bln_login != False:
                    sw=1
                    user.value=""
                    email.value=""
                    password.value=""
                    confirm_password.value=""
                    name.value=""
                    message="Cuenta creada satisfactoriamente"
                    bgcolor="green"
                else:
                    user.error_text="Usuario ya registrado"
                    user.update()
            else:
                confirm_password.error_text="Las contraseñas no coinciden"
                confirm_password.update()
        if message != "":
            settings.message=message
            settings.showMessage(bgcolor)
            if sw == 1:
                loginMe(e)
        else:
            if user.value == "":
                user.error_text="Digite el usuario"
                btn_login.focus()
            if email.value == "":
                email.error_text="Digite el correo electrónico"
                btn_login.focus()
            if password.value == "":
                password.error_text="Digite la contraseña"
                btn_login.focus()
            if confirm_password.value == "":
                confirm_password.error_text="Confirme la contraseña"
                btn_login.focus()
            if name.value == "":
                name.error_text="Digite el nombre"
                btn_login.focus()
            user.update()
            email.update()
            password.update()
            confirm_password.update()
            name.update()

    def sign_up(e):
        lbl_login.value="Crear cuenta"
        user.hint_text="Usuario"
        btn_login.text="Crear cuenta"
        btn_login.on_click=signUp
        email.visible=True
        confirm_password.visible=True
        name.visible=True
        lbl_cuenta.value="Ya tiene una cuenta"
        btn_cuenta.visible=False
        btn_loginme.visible=True
        btn_reset_password.visible=False
        user.value=""
        email.value=""
        password.value=""
        name.value=""
        user.error_text=""
        email.error_text=""
        password.error_text=""
        confirm_password.error_text=""
        name.error_text=""
        settings.page.update()

    def resetPassword(e):
        user.error_text=""
        if user.value != "":
            usuario=user.value
            login_user, correo_electronico, password=reset_password(usuario)
            if login_user == "":
                title="Reestablecer contraseña"
                message="Se ha enviado un código de un solo uso al correo electrónico " + correo_electronico
                open_dlg_modal2(e, title, message)
                send_mail_user(config("EMAIL_USER"), correo_electronico, settings.token_password)
        else:
            user.error_text="Digite usuario ó correo electrónico"
            user.focus()
            page.update()
    
    def logout():
        user.value=""
        password.value=""
        page.session.clear()

    def exit(e):
        logout()
        page.window.close()

    def close_dlg(e):
        dlg_modal.open=False
        page.update()

    def open_dlg_modal(e, title, message):
        # dlg_modal.title=ft.Text(title, text_align="center")
        dlg_modal.title=ft.Row([
            ft.Icon(ft.icons.LOGOUT_ROUNDED, size=32),
            ft.Text(title, text_align="center", color=ft.colors.PRIMARY)
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )
        dlg_modal.content=ft.Text(message, text_align="center")
        page.overlay.append(dlg_modal)
        dlg_modal.open=True
        page.update()

    dlg_modal=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        # icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Sí", on_click=exit),
            ft.TextButton("No", autofocus=True, on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        # on_dismiss=lambda _: date_button.focus(),
    )

    def close_dlg2(e):
        dlg_modal2.open=False
        page.update()

    def open_dlg_modal2(e, title, message):
        dlg_modal2.title=ft.Text(title, text_align="center")
        dlg_modal2.content=ft.Text(message, text_align="center")
        page.overlay.append(dlg_modal2)
        dlg_modal2.open=True
        page.update()

    dlg_modal2=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        icon=ft.Icon(name=ft.icons.INFO_SHARP, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        actions=[
            ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg2)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        # on_dismiss=lambda _: date_button.focus(),
    )

    def validate_email(e):
        dlg_modal3.content.error_text=""
        email = correo.value
        if email == "":
            dlg_modal3.content.error_text="Digite correo electrónico"
            dlg_modal3.update()
            return False
        # if not re.match(email_regex, email):
        #     dlg_modal3.content.error_text="Correo electrónico no válido"
        #     dlg_modal3.update()
        #     return False
        else:
            update_user(settings.username, correo.value, settings.password, settings.photo, "update")
            close_dlg3(e)
            
    correo=ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL, text_align="left")

    def close_dlg3(e):
        correo.value=""
        correo.update()
        dlg_modal3.content.error_text=""
        dlg_modal3.open=False
        dlg_modal3.update()

    def open_dlg_modal_email(e):
        dlg_modal3.title=ft.Row([
                ft.Icon(ft.icons.EMAIL, size=32),
                ft.Text("Correo electrónico", text_align="center", color=ft.colors.PRIMARY)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        # dlg_modal4.title=ft.Text("Correo electrónico", text_align="center")
        # dlg_modal3.content=ft.TextField(label="Correo electrónico", prefix_icon=ft.icons.EMAIL, text_align="left")
        page.overlay.append(dlg_modal3)
        dlg_modal3.open=True
        page.update()

    dlg_modal3=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        # icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
        # title=ft.Text(title, text_align="center"),
        # content=ft.Text(message, text_align="center"),
        content=correo,
        actions=[
            ft.TextButton("Enviar", autofocus=True, on_click=validate_email)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        # on_dismiss=lambda _: sendMailBilling,
    )

    # lbl_login=ft.Text("Iniciar sesión", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
    # user=ft.TextField(width=280, height=60, hint_text="Usuario ó correo electrónico", border="underline", prefix_icon=ft.icons.PERSON_SHARP)
    # email=ft.TextField(width=280, height=60, hint_text="Correo electrónico", border="underline", prefix_icon=ft.icons.EMAIL, visible=False)
    # password=ft.TextField(width=280, height=60, hint_text="Contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    # confirm_password=ft.TextField(width=280, height=60, hint_text="Confirmar contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, visible=False)
    # name=ft.TextField(width=280, height=60, hint_text="Nombre", border="underline", prefix_icon=ft.icons.PERSON_SHARP, visible=False)
    # btn_login=ft.ElevatedButton(text="Iniciar sesión", width=280, bgcolor=ft.colors.BLUE_900, color="white")
    # btn_reset_password=ft.TextButton("¿Olvidó su contraseña?", visible=True if settings.tipo_app == 1 else False)
    # lbl_cuenta=ft.Text("¿No tiene una cuenta?")
    # btn_cuenta=ft.TextButton("Crear cuenta")
    # btn_loginme=ft.TextButton("Iniciar sesión", visible=False)

    lbl_login=ft.Text("Iniciar sesión", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
    user=ft.TextField(width=280, height=60, hint_text="Usuario ó correo electrónico", border="underline", prefix_icon=ft.icons.PERSON_SHARP)
    email=ft.TextField(width=280, height=60, hint_text="Correo electrónico", border="underline", prefix_icon=ft.icons.EMAIL, visible=False)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    confirm_password=ft.TextField(width=280, height=60, hint_text="Confirmar contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, visible=False)
    name=ft.TextField(width=280, height=60, hint_text="Nombre", border="underline", prefix_icon=ft.icons.PERSON_SHARP, visible=False)
    btn_login=ft.ElevatedButton(text="Iniciar sesión", width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=login)
    btn_reset_password=ft.TextButton("¿Olvidó su contraseña?", visible=True if settings.tipo_app == 1 else False, on_click=resetPassword)
    lbl_cuenta=ft.Text("¿No tiene una cuenta?")
    btn_cuenta=ft.TextButton("Crear cuenta", on_click=sign_up)
    btn_loginme=ft.TextButton("Iniciar sesión", visible=False, on_click=loginMe)

    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Stack([
                    ft.Row([
                        ft.Column([
                            ft.Row([
                                ft.Column(
                                    controls=[
                                        ft.Container(
                                            ft.Column([
                                                ft.Container(
                                                    # ft.Text(
                                                    #     "Iniciar sesión",
                                                    #     width=320,
                                                    #     # size=30,
                                                    #     theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                                    #     text_align="center",
                                                    #     # weight="W900",
                                                    #     color=ft.colors.BLUE_900
                                                    # )
                                                    lbl_login,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    user,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    email,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    password,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    confirm_password,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    name,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    btn_login,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    btn_reset_password,
                                                    padding=ft.padding.only(20,20)
                                                ),
                                                ft.Container(
                                                    ft.Row([
                                                        lbl_cuenta,
                                                        btn_cuenta,
                                                        btn_loginme,
                                                    ],
                                                    alignment=ft.MainAxisAlignment.CENTER
                                                    ),
                                                    padding=ft.padding.only(20,20)
                                                )
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                            ),
                                            border_radius=20,
                                            width=320,
                                            # height=500,
                                            height=page.height-70 if settings.tipo_app == 0 else None,
                                            # gradient=ft.LinearGradient([
                                            #     ft.colors.PURPLE,
                                            #     ft.colors.PINK,
                                            #     ft.colors.RED
                                            # ])
                                        )
                                    ]
                                )
                            ])
                        ]),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            ft.Container(height=50),
        ]
    )




    # page.padding=0
    # page.add(container)


    # return ft.Column(
    #     controls=[      
    #         ft.Container(height=20),  
    #         ft.Container(
    #             ft.Column([
    #                 ft.Container(
    #                     ft.Text(
    #                         "Iniciar sesión",
    #                         width=320,
    #                         size=30,
    #                         text_align="center",
    #                         weight="W900",
    #                         color="white"
    #                     ),
    #                     padding=ft.padding.only(20,20)
    #                 ),
    #                 ft.Container(
    #                     user,
    #                     padding=ft.padding.only(20,20)
    #                 ),
    #                 ft.Container(
    #                     password,
    #                     padding=ft.padding.only(20,20)
    #                 ),
    #                 ft.Container(
    #                     ft.ElevatedButton(
    #                         text="Iniciar sesión",
    #                         width=280,
    #                         bgcolor="black",
    #                         color="white",
    #                         on_click=validateUser
    #                     ),
    #                     padding=ft.padding.only(20,20)
    #                 ),
    #                 ft.Container(
    #                     ft.Row([
    #                         ft.Text("¿No tiene una cuenta?"),
    #                         ft.TextButton("Crear cuenta")
    #                     ],
    #                     alignment=ft.MainAxisAlignment.CENTER
    #                     ),
    #                     padding=ft.padding.only(20,20)
    #                 )
    #             ],
    #             alignment=ft.MainAxisAlignment.SPACE_EVENLY
    #             ),
    #             border_radius=20,
    #             width=320,
    #             height=500,
    #             gradient=ft.LinearGradient([
    #                 ft.colors.PURPLE,
    #                 ft.colors.PINK,
    #                 ft.colors.RED
    #             ])
    #         )
    #     ]
    # )





# class Login:

#     # def __init__(self):

    # def main(page:ft.Page):

    #     def validateUser(e):
    #         if user.value != "" and password.value != "":
    #             usuario=user.value
    #             contrasena=password.value
    #             selectUser(usuario, contrasena)
    #             # page.go("/register")
    #         else:
    #             user.focus()

    #     user=ft.TextField(
    #         width=280,
    #         height=40,
    #         hint_text="Usuario",
    #         border="underline",
    #         color="black",
    #         prefix_icon=ft.icons.ACCOUNT_BOX_ROUNDED
    #     )

    #     password=ft.TextField(
    #         width=280,
    #         height=40,
    #         hint_text="Contraseña",
    #         border="underline",
    #         color="black",
    #         prefix_icon=ft.icons.LOCK,
    #         password=True
    #     )
    
    #     container = ft.Container(
    #         ft.Column([
    #             ft.Container(
    #                 ft.Text(
    #                     "Iniciar sesión",
    #                     width=320,
    #                     size=30,
    #                     text_align="center",
    #                     weight="W900",
    #                     color="white"
    #                 ),
    #                 padding=ft.padding.only(20,20)
    #             ),
    #             ft.Container(
    #                 user,
    #                 padding=ft.padding.only(20,20)
    #             ),
    #             ft.Container(
    #                 password,
    #                 padding=ft.padding.only(20,20)
    #             ),
    #             ft.Container(
    #                 ft.ElevatedButton(
    #                     text="Iniciar sesión",
    #                     width=280,
    #                     bgcolor="black",
    #                     color="white",
    #                     on_click=validateUser
    #                 ),
    #                 padding=ft.padding.only(20,20)
    #             ),
    #             ft.Container(
    #                 ft.Row([
    #                     ft.Text("¿No tiene una cuenta?"),
    #                     ft.TextButton("Crear cuenta")
    #                 ],
    #                 alignment=ft.MainAxisAlignment.CENTER
    #                 ),
    #                 padding=ft.padding.only(20,20)
    #             )
    #         ],
    #         alignment=ft.MainAxisAlignment.SPACE_EVENLY
    #         ),
    #         border_radius=20,
    #         width=320,
    #         height=500,
    #         gradient=ft.LinearGradient([
    #             ft.colors.PURPLE,
    #             ft.colors.PINK,
    #             ft.colors.RED
    #         ])
    #     )

    #     page.window_opacity=0.8
    #     page.opacity=0.0
    #     page.bgcolor=ft.colors.BLACK
    #     page.vertical_alignment="center"
    #     page.horizontal_alignment="center"
    #     page.add(container)

    # # # if __name__ == "__main__":
    # # ft.app(target=main)
    # # # ft.app(port=9000, target=main, view=ft.AppView.WEB_BROWSER)