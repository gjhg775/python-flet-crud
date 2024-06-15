import os
import flet as ft
import settings
import hashlib
from pages.login import Login
from pages.home import home
from pages.configuration import Configuration
from pages.variables import Variables
from pages.register import *
from pages.cash_register import *
from pages.closing_day import Closing_day
from pages.developer import Developer
from datatable import get_configuration, selectUser, add_user

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

configuracion=get_configuration()

if configuracion != None:
    parqueadero=configuracion[0][1]
    nit=configuracion[0][2]
    regimen=configuracion[0][3]
    direccion=configuracion[0][4]
    telefono=configuracion[0][5]
    servicio=configuracion[0][6]
    consecutivo=configuracion[0][7]

def main(page: ft.Page):
    
    def change_navigation_destination(e):
        if e.control.selected_index == 0:
            hide_drawer(e)
            page.clean()
            page.add(home(page))
        if e.control.selected_index == 1:
            hide_drawer(e)
            page.clean()
            page.add(Configuration(page))
        if e.control.selected_index == 2:
            hide_drawer(e)
            page.clean()
            page.add(Variables(page))
            page.update()
        if e.control.selected_index == 3:
            hide_drawer(e)
            page.clean()
            page.add(Register(page))
            tblRegistro.scroll="auto"
            tblRegistro.update()
            page.update()
        if e.control.selected_index == 4:
            hide_drawer(e)
            page.clean()
            page.add(Cash_register(page))
            tblCuadre.scroll="auto"
            tblCuadre.update()
            page.update()
        if e.control.selected_index == 5:
            hide_drawer(e)
            page.clean()
            page.add(Closing_day(page))
        if e.control.selected_index == 6:
            hide_drawer(e)
            page.clean()
            page.add(Developer(page))
        if e.control.selected_index == 7:
            logout()
            hide_drawer(e)
            page.clean()
            page.add(container)

    def show_drawer(e):
        if page.session.get("Loginme") != None:
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
        btn_login.text="Iniciar sesión"
        btn_login.on_click=login
        name.visible=False
        lbl_cuenta.value="¿No tiene una cuenta?"
        btn_cuenta.visible=True
        btn_loginme.visible=False
        user.value=""
        password.value=""
        user.error_text=""
        password.error_text=""
        name.error_text=""
        page.update()

    def login(e):
        user.error_text=""
        password.error_text=""
        bln_login=False
        if user.value != "" and password.value != "":
            usuario=user.value
            contrasena=password.value
            login_user, login_password, bln_login=selectUser(usuario, contrasena)
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
                datalogin={"value":True, "username":user.value}
                page.session.set("Loginme", datalogin)
                settings.username=page.session.get('Loginme')
                # page.go("/register")
                page.clean()
                # page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
                page.appbar.title=ft.Text("Parqueadero", color=ft.colors.WHITE)
                page.add(home(page))
                page.update()
                # page.snack_bar=ft.SnackBar(
                #     ft.Text(f"Bienvenido {username['username']}", size=30, text_align="center"),
                #     bgcolor="green"
                # )
                # page.snack_bar.open=True
                # page.update()
            # else:
            #     page.snack_bar=ft.SnackBar(
            #         ft.Text("Acceso denegado", size=30, text_align="center"),
            #         bgcolor="red"
            #     )
            #     page.snack_bar.open=True
            #     page.update()
        else:
            if user.value == "":
                user.error_text="Digite el usuario"
                btn_login.focus()
            if password.value == "":
                password.error_text="Digite la contraseña"
                btn_login.focus()
            user.update()
            password.update()

    def signUp(e):
        message=""
        user.error_text=""
        password.error_text=""
        name.error_text=""
        bln_login=False
        if user.value != "" and password.value != "" and name.value != "":
            usuario=user.value
            contrasena=password.value
            nombre=name.value
            login_user, login_password, bln_login=selectUser(usuario, contrasena)
            if bln_login == False:
                user.error_text=""
                # user.focus()
                # btn_login.focus()
                # user.update()
                hash=hashlib.sha256(contrasena.encode()).hexdigest()
                add_user(usuario, hash, nombre)
                user.value=""
                password.value=""
                name.value=""
                message="Cuenta creada satisfactoriamente"
            else:
                user.error_text="Usuario ya registrado"
                user.update()
        if message != "":
            page.snack_bar=ft.SnackBar(
                ft.Text(message, color="white", text_align="center"),
                bgcolor="green"
            )
            page.snack_bar.open=True
            page.update()
                
            # if login_password != "" and bln_login == False:
            #     password.error_text=login_password
            #     # password.focus()
            #     btn_login.focus()
            #     password.update()
            # else:
            #     password.error_text=""
            #     password.update()
            # if bln_login == True:
            #     datalogin={"value":True, "username":user.value}
            #     page.session.set("Loginme", datalogin)
            #     settings.username=page.session.get('Loginme')
            #     # page.go("/register")
            #     page.clean()
            #     # page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
            #     page.appbar.title=ft.Text("Parqueadero", color=ft.colors.WHITE)
            #     page.add(home(page))
            #     page.update()
            #     # page.snack_bar=ft.SnackBar(
            #     #     ft.Text(f"Bienvenido {username['username']}", size=30, text_align="center"),
            #     #     bgcolor="green"
            #     # )
            #     # page.snack_bar.open=True
            #     # page.update()
            # # else:
            # #     page.snack_bar=ft.SnackBar(
            # #         ft.Text("Acceso denegado", size=30, text_align="center"),
            # #         bgcolor="red"
            # #     )
            # #     page.snack_bar.open=True
            # #     page.update()
        else:
            if user.value == "":
                user.error_text="Digite el usuario"
                btn_login.focus()
            if password.value == "":
                password.error_text="Digite la contraseña"
                btn_login.focus()
            if name.value == "":
                name.error_text="Digite el nombre"
                btn_login.focus()
            user.update()
            password.update()
            name.update()

    def sign_up(e):
        lbl_login.value="Crear cuenta"
        btn_login.text="Crear cuenta"
        btn_login.on_click=signUp
        name.visible=True
        lbl_cuenta.value="Ya tengo una cuenta"
        btn_cuenta.visible=False
        btn_loginme.visible=True
        user.value=""
        password.value=""
        name.value=""
        user.error_text=""
        password.error_text=""
        name.error_text=""
        page.update()
    
    def logout():
        user.value=""
        password.value=""
        page.session.clear()

    mode_switch=ft.Switch(
        value=False,
        on_change=change_mode_theme,
        thumb_color="black",
        thumb_icon={
            ft.MaterialState.DEFAULT: ft.icons.LIGHT_MODE,
            ft.MaterialState.SELECTED: ft.icons.DARK_MODE,
        }
    )

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Inicio",
                icon=ft.icons.HOME_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HOME),
            ),
            ft.Divider(thickness=2),
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
                icon_content=ft.Icon(ft.icons.PERSON_OUTLINED),
                label="Desarrollador",
                selected_icon=ft.icons.PERSON_ROUNDED,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.POWER_SETTINGS_NEW_OUTLINED),
                label="Cerrar sesión",
                selected_icon=ft.icons.POWER_SETTINGS_NEW,
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

    page.title="Parqueadero"
    page.scroll="auto"
    page.theme_mode="light"
    page.window_opacity=0.8
    page.opacity=0.0
    page.window_min_width=378
    # page.window_width=378
    # page.window_width=992
    # page.window_resizable=False
    # page.window_maximizable=False
    page.padding=0
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.window_center()
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
    user=ft.TextField(width=280, height=60, hint_text="Usuario", border="underline", prefix_icon=ft.icons.PERSON_SHARP)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    name=ft.TextField(width=280, height=60, hint_text="Nombre", border="underline", prefix_icon=ft.icons.PERSON_SHARP, visible=False)
    btn_login=ft.ElevatedButton(text="Iniciar sesión", width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=login)
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
                            password,
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

if settings.sw == 0:
    ft.app(target=main)
else:
    ft.app(target=main, port=9000, assets_dir="assets", view=ft.AppView.WEB_BROWSER)


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