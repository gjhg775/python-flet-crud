import flet as ft
from pages.login import Login
from pages.home import Home
from pages.configuration import Configuration
from pages.variables import Variables
from pages.register import *
from pages.developer import Developer
from datatable import get_configuration, selectUser

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
            page.add(Home(page))
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
            # placa.focus()
        if e.control.selected_index == 4:
            hide_drawer(e)
            page.clean()
            page.add(Developer(page))
        if e.control.selected_index == 5:
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
                username=page.session.get('Loginme')
                # page.go("/register")
                page.clean()
                page.appbar.title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE)
                page.add(Home(page))
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
    # page.window_resizable=False
    # page.window_maximizable=False
    page.vertical_alignment="center"
    page.horizontal_alignment="center"
    page.window_center()
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU_SHARP, icon_color=ft.colors.WHITE, on_click=show_drawer),
        leading_width=55,
        # title=ft.Text("Parqueadero", color=ft.colors.WHITE),
        title=ft.Text("Parqueadero "+parqueadero, color=ft.colors.WHITE),
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

    lbl_login=ft.Text("Iniciar sesión", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.BLUE_900)
    user=ft.TextField(width=280, height=60, hint_text="Usuario", border="underline", prefix_icon=ft.icons.PERSON_SHARP)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True)
    btn_login=ft.ElevatedButton(text="Iniciar sesión", width=280, bgcolor=ft.colors.BLUE_900, color="white", on_click=login)

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
                            btn_login,
                            padding=ft.padding.only(20,20)
                        ),
                        ft.Container(
                            ft.Row([
                                ft.Text("¿No tiene una cuenta?"),
                                ft.TextButton("Crear cuenta")
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

ft.app(target=main, assets_dir="assets")
# ft.app(target=main, port=9000, view=ft.AppView.WEB_BROWSER, assets_dir="assets")




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