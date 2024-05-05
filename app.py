import flet as ft
from pages.home import Home
from pages.register import *

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

def main(page: ft.Page):

    def change_navigation_destination(e):
        if e.control.selected_index == 0:
            hide_drawer(e)
            page.clean()
            page.add(Home(page))
        elif e.control.selected_index == 1:
            hide_drawer(e)
            page.clean()
            page.add(Register(page))
            tblRegistro.scroll="auto"
            tblRegistro.update()
            page.update()
            placa.focus()

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
                icon_content=ft.Icon(ft.icons.EDIT_OUTLINED),
                label="Registro",
                selected_icon=ft.icons.EDIT_ROUNDED,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
        on_change=lambda e: change_navigation_destination(e),
    )

    def show_drawer(e):
        page.drawer.open = True
        page.drawer.update()

    def hide_drawer(e):
        page.drawer.open = False
        page.drawer.update()

    # def check_item_clicked(e):
    #     e.control.checked = not e.control.checked
    #     page.update()

    page.title="Parqueadero"
    page.window_opacity=0.8
    page.opacity=0.0
    page.window_resizable=False
    page.window_maximizable=False
    # page.window_center()
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU_SHARP, icon_color=ft.colors.WHITE, on_click=show_drawer),
        leading_width=55,
        title=ft.Text("Parqueadero", color=ft.colors.WHITE),
        center_title=False,
        # bgcolor=ft.colors.PRIMARY_CONTAINER,
        bgcolor=ft.colors.BLUE_900,
        # actions=[
        #     ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
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
        # ],
    )
    page.add(Home(page))

ft.app(target=main)




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