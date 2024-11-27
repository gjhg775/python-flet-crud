import os
import time
import flet as ft
import settings
import hashlib
try:
    from views import views_handler
except Exception as e:
    print(e)
try:
    from pages.login import Login
except Exception as e:
    print(e)
try:
    from pages.profile import Profile
except Exception as e:
    print(e)
try:
    from pages.home import Home
except Exception as e:
    print(e)
try:
    from pages.users import Users
except Exception as e:
    print(e)
try:
    from pages.configuration import Configuration
except Exception as e:
    print(e)
try:
    from pages.variables import Variables
except Exception as e:
    print(e)
try:
    from pages.register import *
except Exception as e:
    print(e)
try:
    from pages.cash_register import *
except Exception as e:
    print(e)
try:
    from pages.closing_day import Closing_day
except Exception as e:
    print(e)
from pages.developer import Developer
try:
    from datatable import get_configuration, selectUser, selectAccess, add_user, get_user, reset_password, update_user, lblAccesos, tba
except Exception as e:
    print(e)
# from decouple import config
from mail import send_mail_user

if settings.tipo_app == 0:
    def main(page:ft.Page):
        # if settings.tipo_app == 0:
        #     settings.user_avatar=ft.Image(src=f"img\\{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
        # else:
        #     settings.user_avatar=ft.Image(src=f"img/{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
        settings.user_avatar=ft.Image(src=f"/img/{settings.photo}", height=70, width=70, fit=ft.ImageFit.COVER, border_radius=150)
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
                    # lblAccesos.update()
                    # page.update()
                else:
                    acceso=0
            if e.control.selected_index == 2:
                hide_drawer(e)
                if settings.acceso_configuracion == 1:
                    page.clean()
                    page.add(Configuration(page))
                    # page.update()
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
        
        def route_change(route):
            page.views.clear()
            page.views.append(
                views_handler(page)[page.route]
            )
            page.update()

        def view_pop(view):
            page.views.pop()
            top_view=page.views[-1]
            page.go(top_view.route)
                
        def show_drawer(e):
            if page.session.get("username") != None:
                page.drawer.open = True
                page.drawer.update()

        def hide_drawer(e):
            page.drawer.open = False
            page.drawer.update()

        def change_mode_theme(e):
            page.theme_mode=ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
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
                        page.session.set("username", datalogin["username"])
                        settings.username=login_user if settings.tipo_app == 0 else page.session.get("username")
                        username=settings.username
                        settings.photo=login_photo
                        if correo_electronico == "":
                            open_dlg_modal_email(e)
                        settings.correo_electronico=correo_electronico
                        selectAccess(username)
                        # page.go("/register")
                        page.clean()
                        # page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
                        # page.appbar.title=ft.Text("Parqueadero", color=ft.colors.WHITE, size=20)
                        page.add(Home(page))
                        page.update()
                        # if settings.tipo_app == 0:
                        #     settings.user_avatar.src=f"img\\{login_photo}"
                        #     settings.user_photo.src=f"img\\{login_photo}"
                        # else:
                        #     settings.user_avatar.src=f"img/{login_photo}"
                        #     settings.user_photo.src=f"img/{login_photo}"
                        settings.user_avatar.src=f"/img/{login_photo}"
                        settings.user_photo.src=f"/img/{login_photo}"
                        settings.login_nombre=login_nombre
                        user_auth.value=settings.login_nombre
                        user_auth.update()
                        settings.message=f"Bienvenido {login_nombre}"
                        bgcolor="blue"
                    else:
                        settings.message="Acceso denegado"
                        bgcolor="red"
                    settings.showMessage(bgcolor)
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
                    # send_mail_user(config("EMAIL_USER"), correo_electronico, settings.token_password)
            else:
                user.error_text="Digite usuario ó correo electrónico"
                user.focus()
                page.update()
        
        def logout():
            user.value=""
            password.value=""
            page.session.clear()
            # page.session.remove("username")
            # page.session.remove("secret_key")

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
            if not re.match(email_regex, email):
                dlg_modal3.content.error_text="Correo electrónico no válido"
                dlg_modal3.update()
                return False
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
                    icon_content=ft.Icon(ft.icons.POWER_SETTINGS_NEW_OUTLINED if settings.tipo_app == 1 else ft.icons.LOGOUT_OUTLINED),
                    label="Cerrar sesión" if settings.tipo_app == 1 else "Salir",
                    selected_icon=ft.icons.POWER_SETTINGS_NEW if settings.tipo_app == 1 else ft.icons.LOGOUT_ROUNDED,
                )
            ],
            on_change=lambda e: change_navigation_destination(e),
            #  if settings.tipo_app == 0 else route_change
        )

        if settings.tipo_app == 1:
            # page.route="/login"
            page.on_route_change=route_change
            page.on_view_pop=view_pop
            page.go(page.route)

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
        page.theme_mode=ft.ThemeMode.LIGHT
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
        
        if settings.tipo_app == 0:
            page.appbar = ft.AppBar(
                # leading=ft.IconButton(ft.icons.MENU_SHARP, icon_color=ft.colors.WHITE, on_click=show_drawer),
                # leading_width=230,
                # title=ft.Text("Parqueadero", color=ft.colors.WHITE),
                leading=ft.ListTile(
                    content_padding=ft.padding.only(top=4),
                    leading=ft.Image(src=f"/img/parqueadero.png", height=55, width=55, fit=ft.ImageFit.COVER),
                    # title=ft.Text("Parqueadero", color=ft.colors.WHITE, size=25),
                    on_click=show_drawer
                ),
                title=ft.Text("Parqueadero", color=ft.colors.WHITE, size=25),
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
        # else:
        #     frame_appbar=ft.Container(
        #         # expand=True,
        #         height=60,
        #         bgcolor=ft.colors.BLUE_900,
        #         # border_radius=10,
        #         alignment=ft.alignment.center,
        #         content=ft.Text("Parqueadero", size=30, color=ft.colors.WHITE),
        #     )
        #     page.overlay.append(frame_appbar)
        #     page.update()

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

        #     frame_menu=ft.Container(
        #         margin=ft.margin.only(top=60),
        #         bgcolor=ft.colors.BLUE_900,
        #         # animate_size=self.animation_style,
        #         width=200,
        #         # border_radius=10,
        #         padding=10,
        #         content=ft.Column(
        #             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        #             controls=[
        #                 ft.Row([
        #                     ft.Container(
        #                         # height=938,
        #                         expand=True,
        #                         width=200,
        #                         # shadow=ft.BoxShadow(
        #                         #     spread_radius=1,
        #                         #     blur_radius=15,
        #                         #     color=ft.colors.BLUE_GREY_300,
        #                         #     offset=ft.Offset(0, 0),
        #                         #     blur_style=ft.ShadowBlurStyle.OUTER,
        #                         # ),
        #                         # expand=2,
        #                         padding=ft.padding.only(0, 20, 0, 0),
        #                         bgcolor=ft.colors.BLUE_900,
        #                         # border_radius=ft.border_radius.all(10),
        #                         # alignment=ft.alignment.center,
        #                         content=ft.Column([
        #                             # btn_profile,
        #                             ft.Container(
        #                                 padding=ft.padding.only(10, 10, 10, 10),
        #                                 on_click=lambda e: settings.page.go("/profile"),
        #                                 content=ft.Row([
        #                                     settings.user_avatar,
        #                                     # settings.page.user_auth
        #                                 ]),
        #                             ),
        #                             ft.Divider(thickness=2),
        #                             btn_home,
        #                             btn_users,
        #                             btn_settings,
        #                             btn_variables,
        #                             btn_register,
        #                             btn_cash_register,
        #                             btn_closing_day,
        #                             ft.Divider(thickness=2),
        #                             btn_developer,
        #                             ft.Divider(thickness=2),
        #                             btn_logout
        #                         ],
        #                         horizontal_alignment="center",
        #                         ),
        #                     ),
        #                     # ft.Container(
        #                     #     expand=10,
        #                     #     padding=ft.padding.only(0, 20, 0, 0),
        #                     #     # bgcolor="blue",
        #                     #     content=ft.Column([
        #                     #         ft.Container(height=100),
        #                     #         developer_photo,
        #                     #         ft.Container(height=100),
        #                     #     ], 
        #                     #     horizontal_alignment="center",
        #                     #     ),
        #                     # )
        #                 ]),
        #             ]
        #         )
        #     )
        #     page.overlay.append(frame_menu)
        #     page.update()

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

        page.padding=0
        page.add(container)
else:
    message=""
    bgcolor=""           
    # class AnimatedApp(ft.UserControl):
    class AnimatedApp(ft.Row):
        def __init__(self, page):
            super().__init__(expand=True)
            self.page=page

            self.page.locale_configuration = ft.LocaleConfiguration(
                supported_locales=[
                    # ft.Locale("de", "DE"),  # German, Germany
                    # ft.Locale("fr", "FR"),  # French, France
                    ft.Locale("es"),        # Spanish
                ],
                current_locale=ft.Locale("es"),
            )

            self.page.title="Parqueadero"
            self.page.theme_mode=ft.ThemeMode.LIGHT
            self.page.padding=0
            self.page.add()

            # snack_bar=ft.SnackBar(
            #     ft.Text(message, text_align="center"),
            #     bgcolor=bgcolor,
            #     duration=2000,
            #     open=True
            # )

            # if message != "":
            #     self.page.add(snack_bar)
            #     self.page.update()

            # self.routes = {
            #     "/": 0,
            #     "/usuarios": 1,
            #     "/configuracion": 2,
            #     "/variables": 3,
            #     "/registro": 4,
            #     "/cuadre_caja": 5,
            #     "/cierre_dia": 6,
            #     "/desarrollador": 7,
            #     # "/cerrar_sesion": 8,
            #     "/login": 8
            # }

            self.routes = {
                "/profile": 0,
                "/": 1,
                "/users": 2,
                "/configuration": 3,
                "/variables": 4,
                "/register": 5,
                "/cash_register": 6,
                "/closing_day": 7,
                "/developer": 8,
                "/login": 9,
            }

            self.color_container=ft.colors.BLUE_900
            self.color_items=ft.colors.BLUE_800
            self.color_selected_item=ft.colors.BLUE_400
            self.color_icons_light=ft.colors.BLACK
            self.color_icons_dark=ft.colors.WHITE
            self.hover_color=ft.colors.BLUE_600

            # self.animation_style=ft.animation.Animation(400, ft.AnimationCurve.EASE_IN_TO_LINEAR)
            self.animation_style=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_TO_LINEAR)

            settings.label_0.color=self.color_icons_dark
            # settings.label_0=ft.Text(settings.user_auth, color=self.color_icons_dark)
            self.label_1=ft.Text("Inicio", color=self.color_icons_dark, width=120)
            self.label_2=ft.Text("Usuarios", color=self.color_icons_dark, width=120)
            self.label_3=ft.Text("Configuración", color=self.color_icons_dark, width=120)
            self.label_4=ft.Text("Variables", color=self.color_icons_dark, width=120)
            self.label_5=ft.Text("Registro", color=self.color_icons_dark, width=120)
            self.label_6=ft.Text("Cuadre de caja", color=self.color_icons_dark, width=120)
            self.label_7=ft.Text("Cierre de día", color=self.color_icons_dark, width=120)
            self.label_8=ft.Text("Desarrollador", color=self.color_icons_dark, width=120)
            self.label_9=ft.Text("Cerrar sesión", color=self.color_icons_dark, width=120)
            self.label_title=ft.Text("Parqueadero", color=self.color_icons_dark, size=30)
            self.logo=ft.Image(src=f"/img/parqueadero.png", height=50, width=50, fit=ft.ImageFit.COVER, border_radius=150)

            self.mode_switch=ft.Switch(value=True, on_change=self.mode_change_update)

            # self.mode_switch=ft.Switch(
            #     value=True,
            #     on_change=self.mode_change_update,
            #     thumb_color=self.color_selected_item,
            #     track_color=self.color_items,
            #     thumb_icon={
            #         ft.MaterialState.DEFAULT: ft.icons.LIGHT_MODE,
            #         ft.MaterialState.SELECTED: ft.icons.DARK_MODE,
            #     },
            # )

            self.btn_home=ft.Container(
                width=70,
                height=60,
                bgcolor=self.color_container,
                # on_hover=lambda e: self.on_hover_change(e, -1),
                # border_radius=10,
                alignment=ft.alignment.center,
                # content=ft.IconButton(icon=ft.icons.MENU,
                #                     icon_color=self.color_icons_dark,
                #                     on_click=self.bar_icons)
                content=ft.ListTile(
                    content_padding=ft.padding.only(left=15, top=6, right=15, bottom=4),
                    leading=ft.Image(src=f"/img/parqueadero.png", height=55, width=55, fit=ft.ImageFit.COVER),
                    # title=ft.Text("Parqueadero", color=ft.colors.WHITE, size=25),
                    on_click=self.bar_icons
                ),
            )

            self.container_0=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    scroll="auto",
                    controls=[
                        # ft.Text("Inicio"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ],
                    horizontal_alignment="center"
                )
            )

            self.container_1=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Usuarios"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_2=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    scroll="auto",
                    controls=[
                        # ft.Text("Usuarios"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_3=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    scroll="auto",
                    controls=[
                        # ft.Text("Configuración"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_4=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Variables"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_5=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Registro"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_6=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Cuadre de caja"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_7=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Cierre de día"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_8=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Desarrollador"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.container_9=ft.Container(
                # bgcolor=self.color_container,
                offset=ft.transform.Offset(0, 0),
                # animate_offset=self.animation_style,
                border_radius=10,
                padding=10,
                content=ft.Column(
                    controls=[
                        # ft.Text("Cerrar sesión"),
                        # ft.Container(
                        #     border_radius=20,
                        # )
                    ]
                )
            )

            self.switch_control={
                0:self.container_0,
                1:self.container_1,
                2:self.container_2,
                3:self.container_3,
                4:self.container_4,
                5:self.container_5,
                6:self.container_6,
                7:self.container_7,
                8:self.container_8,
                9:self.container_9,
            }

            self.option_0=ft.Container(
                # bgcolor=self.color_items,
                # border_radius=ft.border_radius.only(top_left=0,
                #                             top_right=20,
                #                             bottom_left=0,
                #                             bottom_right=20),
                # animate_scale=self.animation_style,
                # on_click=lambda e: self.change_page(e, 0),
                # on_hover=lambda e: self.on_hover_change(e, 0),
                # height=40,
                # padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    # spacing=20,
                    controls=[
                        ft.Container(
                            # padding=ft.padding.only(top=10),
                            # on_click=lambda e: profile(e),
                            on_click=lambda e: self.change_page(e, 0),
                            # on_hover=lambda e: self.on_hover_change(e, 0),
                            content=ft.Column([
                                settings.user_avatar,
                                settings.label_0
                            ],
                            horizontal_alignment="center"
                            ),
                        ),
                    ],
                )
            )

            self.option_1=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 1),
                on_hover=lambda e: self.on_hover_change(e, 1),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.HOME, color=self.color_icons_dark),
                        # ft.Text("Usuarios", width=120)
                        self.label_1
                    ]
                )
            )

            self.option_2=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 2),
                on_hover=lambda e: self.on_hover_change(e, 2),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.PERSON_ROUNDED, color=self.color_icons_dark),
                        # ft.Text("Usuarios", width=120)
                        self.label_2
                    ]
                )
            )

            self.option_3=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 3),
                on_hover=lambda e: self.on_hover_change(e, 3),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.SETTINGS, color=self.color_icons_dark),
                        # ft.Text("Configuración", width=120)
                        self.label_3
                    ]
                )
            )

            self.option_4=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 4),
                on_hover=lambda e: self.on_hover_change(e, 4),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.FACT_CHECK, color=self.color_icons_dark),
                        # ft.Text("Variables", width=120)
                        self.label_4
                    ]
                )
            )

            self.option_5=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 5),
                on_hover=lambda e: self.on_hover_change(e, 5),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.EDIT_ROUNDED, color=self.color_icons_dark),
                        # ft.Text("Registro", width=120)
                        self.label_5
                    ]
                )
            )

            self.option_6=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 6),
                on_hover=lambda e: self.on_hover_change(e, 6),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.ATTACH_MONEY_SHARP, color=self.color_icons_dark),
                        # ft.Text("Cuadre de caja", width=120)
                        self.label_6
                    ]
                )
            )

            self.option_7=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 7),
                on_hover=lambda e: self.on_hover_change(e, 7),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.CALENDAR_MONTH, color=self.color_icons_dark),
                        # ft.Text("Cierre de día", width=120)
                        self.label_7
                    ]
                )
            )

            self.option_8=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 8),
                on_hover=lambda e: self.on_hover_change(e, 8),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.CODE_ROUNDED, color=self.color_icons_dark),
                        # ft.Text("Desarrollador", width=120)
                        self.label_8
                    ]
                )
            )

            self.option_9=ft.Container(
                bgcolor=self.color_items,
                border_radius=ft.border_radius.only(top_left=0,
                                            top_right=20,
                                            bottom_left=0,
                                            bottom_right=20),
                animate_scale=self.animation_style,
                on_click=lambda e: self.change_page(e, 9),
                on_hover=lambda e: self.on_hover_change(e, 9),
                height=40,
                padding=10,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.icons.POWER_SETTINGS_NEW, color=self.color_icons_dark),
                        # ft.Text("Desarrollador", width=120)
                        self.label_9
                    ]
                )
            )

            self.frame_title=ft.Container(
                expand=True,
                height=60,
                bgcolor=self.color_container,
                # border_radius=10,
                alignment=ft.alignment.center,
                # padding=ft.padding.only(left=15),
                # content=ft.Text("Parqueadero", color=self.color_icons_dark, size=30)
                content=ft.Row([
                    # self.logo,
                    self.label_title
                ],
                alignment=ft.MainAxisAlignment.START,
                )
            )

            self.navigation=ft.Container(
                bgcolor=self.color_container,
                animate_size=self.animation_style,
                width=200,
                # border_radius=10,
                padding=10,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        # ft.Column([
                        #     ft.Container(height=5),
                        #     settings.user_avatar,
                        #     settings.user_auth,
                        # ],
                        # horizontal_alignment="center"
                        # ),
                        # ft.Container(
                        #     padding=ft.padding.only(top=10),
                        #     # on_click=lambda e: profile(e),
                        #     on_click=lambda e: self.change_page(e, 9),
                        #     # on_hover=lambda e: self.on_hover_change(e, 9),
                        #     content=ft.Column([
                        #         settings.user_avatar,
                        #         self.label_user_auth
                        #     ],
                        #     horizontal_alignment="center"
                        #     ),
                        # ),
                        ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                self.option_0,
                                self.option_1,
                                self.option_2,
                                self.option_3,
                                self.option_4,
                                self.option_5,
                                self.option_6,
                                self.option_7,
                                self.option_8,
                                self.option_9,
                            ]
                        )
                    ),
                    self.mode_switch,
                    ]
                )
            )

            self.frame=ft.Container(
                expand=True,
                content=ft.Stack(
                    controls=[
                        self.container_0,
                        self.container_1,
                        self.container_2,
                        self.container_3,
                        self.container_4,
                        self.container_5,
                        self.container_6,
                        self.container_7,
                        self.container_8,
                        self.container_9,
                    ]
                )
            )

            self.page.on_route_change = self.route_change

            self.page.add(ft.Column(
                spacing=0,
                expand=True,
                controls=[
                    ft.Row(
                        spacing=0,
                        controls=[
                            self.btn_home,
                            self.frame_title,
                        ]
                    ),
                    ft.Row(
                        spacing=0,
                        expand=True,
                        controls=[
                            self.navigation,
                            self.frame,
                        ]
                    ),
                ]
            ))

            self.btn_home.visible=False
            self.frame_title.visible=False
            self.navigation.visible=False
            self.page.route="/login"
            self.page.go(self.page.route)
        
        def on_hover_change(self, e, index):
            # Cambia el color del fondo cuando el mouse pasa sobre una opción
            # option = self.switch_control[index]
            # if index == -1:
            #     option = self.btn_home.content
            if index == 0:
                option = self.option_0
            if index == 1:
                option = self.option_1
            if index == 2:
                option = self.option_2
            if index == 3:
                option = self.option_3
            if index == 4:
                option = self.option_4
            if index == 5:
                option = self.option_5
            if index == 6:
                option = self.option_6
            if index == 7:
                option = self.option_7
            if index == 8:
                option = self.option_8
            if index == 9:
                option = self.option_9
            if e.data == "true":
                option.bgcolor = self.hover_color if option.bgcolor != self.color_selected_item else self.color_selected_item # Color al hacer hover
            else:
                option.bgcolor = self.color_items if option.bgcolor != self.color_selected_item else self.color_selected_item # Color por defecto
            option.update()

        def bar_icons(self, e):
            # if e.control.icon == "menu":
            #     self.btn_home.content.icon=ft.icons.HOME
            #     self.navigation.width=200
            # elif e.control.icon == "home":
            #     self.btn_home.content.icon=ft.icons.MENU
            #     self.navigation.width=70
            # self.btn_home.update()
            # self.navigation.update()

            if self.navigation.width == 200:
                self.navigation.width=70
                # settings.user_auth.visible=False
                settings.user_avatar.height=50
                settings.user_avatar.width=50
                settings.label_0.visible=False
            else:
                self.navigation.width=200
                # settings.user_auth.visible=True
                settings.user_avatar.height=70
                settings.user_avatar.width=70
                settings.label_0.visible=True
            self.btn_home.update()
            self.navigation.update()

        def mode_change_update(self, e):
            if e.control.value:
                self.page.theme_mode=ft.ThemeMode.LIGHT
                # settings.user_auth.color=self.color_icons_dark
                # self.option_0.content.controls[0].color=self.color_icons_dark
                self.option_1.content.controls[0].color=self.color_icons_dark
                self.option_2.content.controls[0].color=self.color_icons_dark
                self.option_3.content.controls[0].color=self.color_icons_dark
                self.option_4.content.controls[0].color=self.color_icons_dark
                self.option_5.content.controls[0].color=self.color_icons_dark
                self.option_6.content.controls[0].color=self.color_icons_dark
                self.option_7.content.controls[0].color=self.color_icons_dark
                self.option_8.content.controls[0].color=self.color_icons_dark
                self.option_9.content.controls[0].color=self.color_icons_dark
                self.btn_home.content.icon_color=self.color_icons_dark
                settings.label_0.color=self.color_icons_dark
                self.label_1.color=self.color_icons_dark
                self.label_2.color=self.color_icons_dark
                self.label_3.color=self.color_icons_dark
                self.label_4.color=self.color_icons_dark
                self.label_5.color=self.color_icons_dark
                self.label_6.color=self.color_icons_dark
                self.label_7.color=self.color_icons_dark
                self.label_8.color=self.color_icons_dark
                self.label_9.color=self.color_icons_dark
                self.label_title.color=self.color_icons_dark
            else:
                self.page.theme_mode=ft.ThemeMode.DARK
                # settings.user_auth.color=self.color_icons_light
                # self.option_0.content.controls[0].color=self.color_icons_light
                self.option_1.content.controls[0].color=self.color_icons_light
                self.option_2.content.controls[0].color=self.color_icons_light
                self.option_3.content.controls[0].color=self.color_icons_light
                self.option_4.content.controls[0].color=self.color_icons_light
                self.option_5.content.controls[0].color=self.color_icons_light
                self.option_6.content.controls[0].color=self.color_icons_light
                self.option_7.content.controls[0].color=self.color_icons_light
                self.option_8.content.controls[0].color=self.color_icons_light
                self.option_9.content.controls[0].color=self.color_icons_light
                self.btn_home.content.icon_color=self.color_icons_light
                settings.label_0.color=self.color_icons_light
                self.label_1.color=self.color_icons_light
                self.label_2.color=self.color_icons_light
                self.label_3.color=self.color_icons_light
                self.label_4.color=self.color_icons_light
                self.label_5.color=self.color_icons_light
                self.label_6.color=self.color_icons_light
                self.label_7.color=self.color_icons_light
                self.label_8.color=self.color_icons_light
                self.label_9.color=self.color_icons_light
                self.label_title.color=self.color_icons_light
            self.page.update()

        def change_page(self, e, n):
            if n == 9:
                self.btn_home.visible=False
                self.frame_title.visible=False
                self.navigation.visible=False
            else:
                self.btn_home.visible=True
                self.frame_title.visible=True
                self.navigation.visible=True

            settings.acceso=1
            if n == 2 and settings.acceso_usuarios == 0:
                settings.acceso=0
            if n == 3 and settings.acceso_configuracion == 0:
                settings.acceso=0
            if n == 4 and settings.acceso_variables == 0:
                settings.acceso=0
            if n == 5 and settings.acceso_registro == 0:
                settings.acceso=0
            if n == 6 and settings.acceso_cuadre == 0:
                settings.acceso=0
            if n == 7 and settings.acceso_cierre == 0:
                settings.acceso=0

            if settings.acceso == 1:
                for route, idx in self.routes.items():
                    if idx == n:
                        self.page.go(route)
                        break
                for pag in self.switch_control:
                    self.switch_control[pag].offset.y=2
                    self.switch_control[pag].update()
                    # self.option_0.bgcolor=self.color_items
                    self.option_1.bgcolor=self.color_items
                    self.option_2.bgcolor=self.color_items
                    self.option_3.bgcolor=self.color_items
                    self.option_4.bgcolor=self.color_items
                    self.option_5.bgcolor=self.color_items
                    self.option_6.bgcolor=self.color_items
                    self.option_7.bgcolor=self.color_items
                    self.option_8.bgcolor=self.color_items
                    self.option_9.bgcolor=self.color_items
                if n == 0:
                    # self.option_0.scale=1.2
                    # self.option_0.bgcolor=self.color_selected_item
                    # self.option_0.update()
                    
                    # self.container_0.content.controls.clear()
                    self.container_0.content.controls=[]
                    self.container_0.content.controls.append(Profile(pag))
                    self.container_0.update()
                elif n == 1:
                    self.option_1.scale=1.2
                    self.option_1.bgcolor=self.color_selected_item
                    self.option_1.update()

                    # self.container_1.content.controls.clear()
                    self.container_1.content.controls=[]
                    self.container_1.content.controls.append(Home(pag))
                    self.container_1.update()
                elif n == 2:
                    self.option_2.scale=1.2
                    self.option_2.bgcolor=self.color_selected_item
                    self.option_2.update()

                    # self.container_2.content.controls.clear()
                    self.container_2.content.controls=[]
                    self.container_2.content.controls.append(Users(pag))
                    self.container_2.update()
                elif n == 3:
                    self.option_3.scale=1.2
                    self.option_3.bgcolor=self.color_selected_item
                    self.option_3.update()

                    # self.container_3.content.controls.clear()
                    self.container_3.content.controls=[]
                    self.container_3.content.controls.append(Configuration(pag))
                    self.container_3.update()
                elif n == 4:
                    self.option_4.scale=1.2
                    self.option_4.bgcolor=self.color_selected_item
                    self.option_4.update()

                    # self.container_4.content.controls.clear()
                    self.container_4.content.controls=[]
                    self.container_4.content.controls.append(Variables(pag))
                    self.container_4.update()
                elif n == 5:
                    self.option_5.scale=1.2
                    self.option_5.bgcolor=self.color_selected_item
                    self.option_5.update()

                    # self.container_5.content.controls.clear()
                    self.container_5.content.controls=[]
                    self.container_5.content.controls.append(Register(pag))
                    self.container_5.update()
                elif n == 6:
                    self.option_6.scale=1.2
                    self.option_6.bgcolor=self.color_selected_item
                    self.option_6.update()

                    # self.container_6.content.controls.clear()
                    self.container_6.content.controls=[]
                    self.container_6.content.controls.append(Cash_register(pag))
                    self.container_6.update()
                elif n == 7:
                    self.option_7.scale=1.2
                    self.option_7.bgcolor=self.color_selected_item
                    self.option_7.update()

                    # self.container_7.content.controls.clear()
                    self.container_7.content.controls=[]
                    self.container_7.content.controls.append(Closing_day(pag))
                    self.container_7.update()
                elif n == 8:
                    self.option_8.scale=1.2
                    self.option_8.bgcolor=self.color_selected_item
                    self.option_8.update()

                    # self.container_8.content.controls.clear()
                    self.container_8.content.controls=[]
                    self.container_8.content.controls.append(Developer(pag))
                    self.container_8.update()
                elif n == 9:
                    self.option_9.scale=1.2
                    self.option_9.bgcolor=self.color_selected_item
                    self.option_9.update()

                    # user.value=""
                    # password.value=""
                    settings.username=""
                    settings.password=""
                    settings.user_avatar.src=f"img/default.jpg"
                    settings.label_0.value=""
                    self.page.session.clear()
                    # self.page.session.remove("username")
                    # self.page.session.remove("secret_key")
                    # self.container_9.content.controls.clear()
                    self.container_9.content.controls=[]
                    self.container_9.content.controls.append(Login(pag))
                    self.container_9.update()

                self.switch_control[n].offset.y=0
                self.switch_control[n].update()

                # time.sleep(0.5)
                time.sleep(0.1)

                self.option_0.scale=1
                self.option_1.scale=1
                self.option_2.scale=1
                self.option_3.scale=1
                self.option_4.scale=1
                self.option_5.scale=1
                self.option_6.scale=1
                self.option_7.scale=1
                self.option_8.scale=1
                self.option_9.scale=1

                self.page.update()
                settings.page=self.page
            else:
                bgcolor="orange"
                message="Acceso no permitido"
                settings.message=message
                settings.showMessage(bgcolor)

        def route_change(self, e):
            # Lógica para cambiar la página según la ruta
            if settings.username != "":
                route=self.page.route
                if route in self.routes:
                    self.change_page(None, self.routes[route])
                else:
                    # Si la ruta no existe, redirigir a una ruta predeterminada
                    self.page.go("/")
                    self.change_page(None, 0)
            else:
                self.change_page(None, 9)
        
        # def logout(self, e):
        #     # user.value=""
        #     # password.value=""
        #     # page.session.clear()
        #     self.page.go("/login")
        #     self.change_page(None, 9)

# if __name__ == "__main__":
if settings.tipo_app == 0:
    ft.app(target=main, assets_dir="assets")
else:
    # ft.app(target=main, assets_dir="assets", port=9000, view=ft.AppView.WEB_BROWSER)
    ft.app(target=AnimatedApp, assets_dir="assets", route_url_strategy="path", port=9000, view=ft.WEB_BROWSER)