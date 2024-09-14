import os
import flet as ft
import settings
import hashlib
from pages.login import Login
from pages.profile import Profile
from pages.home import Home
from pages.users import Users
from pages.configuration import Configuration
from pages.variables import Variables
from pages.register import *
from pages.cash_register import *
from pages.closing_day import Closing_day
from pages.developer import Developer
from datatable import get_configuration, selectUser, selectAccess, add_user, get_user, reset_password, lblAccesos, tba
from decouple import config
from mail import send_mail_user

# def main(page: ft.Page):
#     page.drawer = ft.NavigationDrawer(
#         controls=[
#             ft.Container(height=12),
#             ft.NavigationDrawerDestination(
#                 label="Item 1",
#                 icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
#                 selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
#             ),
#             ft.Divider(thickness=2),
#             ft.NavigationDrawerDestination(
#                 icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
#                 label="Item 2",
#                 selected_icon=ft.icons.MAIL,
#             ),
#             ft.NavigationDrawerDestination(
#                 icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
#                 label="Item 3",
#                 selected_icon=ft.icons.PHONE,
#             ),
#         ],
#     )

#     def show_drawer(e):
#         page.drawer.open = True
#         page.drawer.update()

#     page.add(ft.ElevatedButton("Show drawer", on_click=show_drawer))


# ft.app(main)

# configuracion=get_configuration()

# if configuracion != None:
#     parqueadero=configuracion[0][1]
#     nit=configuracion[0][2]
#     regimen=configuracion[0][3]
#     direccion=configuracion[0][4]
#     telefono=configuracion[0][5]
#     servicio=configuracion[0][6]
#     resolucion=configuracion[0][7]
#     desde=configuracion[0][8]
#     hasta=configuracion[0][9]
#     autoriza=configuracion[0][10]
#     consecutivo=configuracion[0][11]

def main(page:ft.Page):
    
    # username=settings.username
    # get_user(username)
    # settings.user_avatar.src=f"upload\\img\\{photo}"
    # settings.user_photo.src=f"upload\\img\\{photo}"
    # page.update()

    if settings.tipo_app == 0:
    #     avatar=ft.Image(src=os.path.join(os.getcwd(), f"upload\\img\\{settings.photo}") if settings.photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
        settings.user_avatar=ft.Image(src=f"upload\\img\\{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    else:
    #     avatar=ft.Image(src=f"img/{settings.photo}" if settings.photo != "" else f"img/default.jpg", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
        settings.user_avatar=ft.Image(src=f"img/{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
    # settings.user_photo=ft.Image(src=f"img/default.jpg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    user_auth=ft.Text("")

    def profile(e):
        hide_drawer(e)
        page.clean()
        page.add(Profile(page))
    
    def change_navigation_destination(e):
        # settings.progressRing.visible=True
        acceso=1
        if e.control.selected_index == 0:
            hide_drawer(e)
            page.clean()
            page.add(Home(page))
        if e.control.selected_index == 1:
            hide_drawer(e)
            if settings.acceso_usuarios == 1:
                page.clean()
                page.add(Users(page))
                lblAccesos.value="Accesos"
                tba.rows.clear()
                page.update()
            else:
                acceso=0
        if e.control.selected_index == 2:
            hide_drawer(e)
            if settings.acceso_configuracion == 1:
                page.clean()
                page.add(Configuration(page))
                # lblAccesos.value="Accesos"
                # tba.rows.clear()
                page.update()
            else:
                acceso=0
        if e.control.selected_index == 3:
            hide_drawer(e)
            if settings.acceso_variables == 1:
                page.clean()
                page.add(Variables(page))
                # page.update()
            else:
                acceso=0
        if e.control.selected_index == 4:
            hide_drawer(e)
            if settings.acceso_registro == 1:
                page.clean()
                page.add(Register(page))
                tblRegistro.scroll="auto"
                tblRegistro.update()
                page.update()
            else:
                acceso=0
        if e.control.selected_index == 5:
            hide_drawer(e)
            if settings.acceso_cuadre == 1:
                page.clean()
                page.add(Cash_register(page))
                tblCuadre.scroll="auto"
                tblCuadre.update()
                page.update()
            else:
                acceso=0
        if e.control.selected_index == 6:
            hide_drawer(e)
            if settings.acceso_cierre == 1:
                page.clean()
                page.add(Closing_day(page))
            else:
                acceso=0
        if e.control.selected_index == 7:
            hide_drawer(e)
            page.clean()
            page.add(Developer(page))
        if e.control.selected_index == 8:
            if settings.tipo_app == 0:
                page.drawer.open = False
                page.drawer.update()
                title="Salir"
                message="Desea salir de la aplicación ?"
                open_dlg_modal(e, title, message)
            else:
                # hide_drawer(e)
                page.drawer.open = False
                page.drawer.update()
                logout()
                page.clean()
                page.add(container)
        if acceso == 0:
            message="Acceso no permitido"
            bgcolor="orange"
            settings.message=message
            settings.showMessage(bgcolor)
        # time.sleep(1)
        # settings.progressRing.visible=False
        # page.update()
            
    def show_drawer(e):
        if page.session.get("username") != None:
            page.drawer.open = True
            page.drawer.update()

    def hide_drawer(e):
        page.drawer.open = False
        page.drawer.update()

    def change_mode_theme(e):
        page.theme_mode="light" if page.theme_mode == "dark" else "dark"
        toggledarklight.selected = not toggledarklight.selected
        page.update()

    # def check_item_clicked(e):
    #     e.control.checked = not e.control.checked
    #     page.update()

    # def validateUser(e):
    #     user.error_text=""
    #     password.error_text=""
    #     if user.value == "":
    #         user.error_text="Digite el usuario"
    #     if password.value == "":
    #         password.error_text="Digite la contraseña"
    #     user.update()
    #     password.update()
    #     if user.error_text != "" and password.error_text != "":
    #         user.focus()
    #         user.update()
    #     elif user.error_text != "" and password.error_text == "":
    #         user.focus()
    #         user.update()
    #     elif user.error_text == "" and password.error_text != "":
    #         password.focus()
    #         password.update()
    #     else:
    #         login()

        # if user.error_text != "" and password.error_text != "":
        #     btn_login.focus()
        #     # user.update()
        # if user.error_text != "" and password.error_text == "":
        #     btn_login.focus()
        #     # user.update()
        # if user.error_text == "" and password.error_text != "":
        #     btn_login.focus()
        #     # password.update()
        # # user.update()
        # # password.update()
        # page.update()
        # if user.error_text == "" and password.error_text == "":
        #     login()

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
        page.update()

    def login(e):
        user.error_text=""
        password.error_text=""
        email.visible=False
        bln_login=False
        if user.value != "" and password.value != "":
            usuario=user.value
            contrasena=str(password.value)
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
                page.session.set("username", datalogin["username"])
                settings.username=page.session.get("username")
                username=settings.username
                settings.photo=login_photo
                settings.correo_electronico=correo_electronico
                selectAccess(username)
                # page.go("/register")
                page.clean()
                # page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
                page.appbar.title=ft.Text("Parqueadero", color=ft.colors.WHITE)
                page.add(Home(page))
                page.update()
                if settings.tipo_app == 0:
                    settings.user_avatar.src=f"upload\\img\\{login_photo}"
                    settings.user_photo.src=f"upload\\img\\{login_photo}"
                else:
                    settings.user_avatar.src=f"img/{login_photo}"
                    settings.user_photo.src=f"img/{login_photo}"
                settings.login_nombre=login_nombre
                user_auth.value=settings.login_nombre
                user_auth.update()
                settings.message=f"Bienvenido {login_nombre}"
                bgcolor="blue"
            else:
                settings.message="Acceso denegado"
                bgcolor="red"
            settings.showMessage(bgcolor)
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
                foto="default.jpg"
                bln_login=add_user(usuario, correo_electronico, hash, nombre, foto)
                if bln_login != False:
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
        page.update()

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
        dlg_modal.title=ft.Text(title, text_align="center")
        dlg_modal.content=ft.Text(message, text_align="center")
        page.overlay.append(dlg_modal)
        dlg_modal.open=True
        page.update()

    dlg_modal=ft.AlertDialog(
        bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.PRIMARY_CONTAINER),
        modal=True,
        icon=ft.Icon(name=ft.icons.QUESTION_MARK, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_900), size=50),
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

    # mode_switch=ft.Switch(
    #     value=False,
    #     on_change=change_mode_theme,
    #     thumb_color="black",
    #     thumb_icon={
    #         ft.MaterialState.DEFAULT: ft.icons.LIGHT_MODE,
    #         ft.MaterialState.SELECTED: ft.icons.DARK_MODE,
    #     }
    # )

    page.drawer = ft.NavigationDrawer(
        controls=[
            # ft.Container(height=12),
            ft.Container(
                padding=ft.padding.only(10, 10, 10, 10),
                on_click=lambda e: profile(e),
                content=ft.Row([
                    settings.user_avatar,
                    user_auth
                ]),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                label="Inicio",
                icon=ft.icons.HOME_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HOME),
            ),
            # ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PERSON_OUTLINED),
                label="Usuarios",
                selected_icon=ft.icons.PERSON_ROUNDED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.SETTINGS_OUTLINED),
                label="Configuración",
                selected_icon=ft.icons.SETTINGS,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.FACT_CHECK_OUTLINED),
                label="Variables",
                selected_icon=ft.icons.FACT_CHECK,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.EDIT_OUTLINED),
                label="Registro",
                selected_icon=ft.icons.EDIT_ROUNDED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.ATTACH_MONEY_OUTLINED),
                label="Cuadre de caja",
                selected_icon=ft.icons.ATTACH_MONEY_SHARP,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED),
                label="Cierre de día",
                selected_icon=ft.icons.CALENDAR_MONTH,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.CODE_OUTLINED),
                label="Desarrollador",
                selected_icon=ft.icons.CODE_ROUNDED,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.POWER_SETTINGS_NEW_OUTLINED if settings.tipo_app == 1 else ft.icons.EXIT_TO_APP_OUTLINED),
                label="Cerrar sesión" if settings.tipo_app == 1 else "Salir",
                selected_icon=ft.icons.POWER_SETTINGS_NEW if settings.tipo_app == 1 else ft.icons.EXIT_TO_APP_ROUNDED,
            )
        ],
        on_change=lambda e: change_navigation_destination(e),
    )

    toggledarklight=ft.IconButton(
        on_click=change_mode_theme,
        icon=ft.icons.DARK_MODE,
        selected_icon=ft.icons.LIGHT_MODE,
        style=ft.ButtonStyle(
            color={"":ft.colors.WHITE, "selected":ft.colors.WHITE}
        )
    )

    settings.page=page
    page.title="Parqueadero"
    page.scroll="auto"
    page.theme_mode="light"
    page.window.opacity=0.8
    page.opacity=0.0
    page.window.min_width=378
    # page.window_width=378
    # page.window_width=992
    # page.window_resizable=False
    # page.window_maximizable=False
    page.padding=0
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.window.center()
    page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                # ft.Locale("de", "DE"),  # German, Germany
                # ft.Locale("fr", "FR"),  # French, France
                ft.Locale("es"),        # Spanish
            ],
            current_locale=ft.Locale("es"),
        )
    page.appbar = ft.AppBar(
            leading=ft.IconButton(ft.icons.MENU_SHARP, icon_color=ft.colors.WHITE, on_click=show_drawer),
            leading_width=55,
            title=ft.Text("Parqueadero", color=ft.colors.WHITE),
            # title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE),
            center_title=False,
            # bgcolor=ft.colors.PRIMARY_CONTAINER,
            bgcolor=ft.colors.BLUE_900,
            actions=[
                toggledarklight,
                # mode_switch
                # ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, icon_color="white", padding=ft.padding.only(right=20), on_click=change_mode_theme),
            #     ft.IconButton(ft.icons.FILTER_3),
            #     ft.PopupMenuButton(
            #         items=[
            #             ft.PopupMenuItem(text="Registro"),
            #             ft.PopupMenuItem(),  # divider
            #             ft.PopupMenuItem(
            #                 text="Checked item", checked=False, on_click=check_item_clicked
            #             ),
            #         ]
            #     ),
            ft.Container(width=10)
            ],
        )

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

    container=ft.Column(
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
                    height=page.height-70,
                    # gradient=ft.LinearGradient([
                    #     ft.colors.PURPLE,
                    #     ft.colors.PINK,
                    #     ft.colors.RED
                    # ])
                )
            ]
        )

    # container=ft.Row([
    #     ft.Column([
    #         lbl_login,
    #         user,
    #         password,
    #         btn_login
    #     ],
    #     alignment=ft.MainAxisAlignment.CENTER,
    #     horizontal_alignment=ft.alignment.center
    #     )
    # ],
    # alignment=ft.MainAxisAlignment.CENTER,
    # )

    # page.add(Home(page))
    page.add(container)

if __name__ == "__main__":
    if settings.tipo_app == 0:
        ft.app(target=main, assets_dir="assets", upload_dir="upload")
    else:
        ft.app(target=main, port=9000, assets_dir="assets", upload_dir="upload", view=ft.AppView.WEB_BROWSER)


# import flet as ft
# from views import views_handler

# def main(page:ft.Page):
#     page.title="Parqueadero"
    
#     def route_change(route):
#         page.views.clear()
#         page.views.append(
#             views_handler(page)[page.route]
#         )
#         page.update()

#     def view_pop(view):
#         page.views.pop()
#         top_view=page.views[-1]
#         page.go(top_view.route)

#     page.on_route_change=route_change
#     page.on_view_pop=view_pop
#     page.go(page.route)
    
#     # page.window_opacity=0.8
#     # page.opacity=0.0
#     # page.bgcolor=ft.colors.BLACK
#     # page.vertical_alignment="center"
#     # page.horizontal_alignment="center"
#     # page.add()

# ft.app(target=main)
# # ft.app(port=9000, target=main, view=ft.AppView.WEB_BROWSER)