import flet as ft
import settings
# from datatable import get_configuration

# parqueadero, regimen=get_configuration()

# class Home(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#     def build(self):
#         return ft.ResponsiveRow(
#             controls=[
#                 # ft.Container(
#                 #     padding=5,
#                 #     col={"sm":0, "md":1, "xl":2},
#                 # ),
#                 ft.Container(
#                     # padding=5,
#                     # col={"sm":6, "md":6, "xl":4},
#                     # alignment=ft.alignment.center,
#                     # content=ft.Stack([
#                         # ft.ResponsiveRow([
#                         #     ft.Column([
#                         #         # ft.ElevatedButton("Registro", on_click=showInputs)
#                         #     ])
#                         # ], 
#                         # alignment=ft.MainAxisAlignment.CENTER,
#                         # ),
#                         # ft.ElevatedButton("Inicio", on_click=lambda _:self.page.go("/"), icon=ft.icons.HOME),
#                         # ft.Row([
#                         #     tblRegistro,
#                         #     card
#                         # ]),                        
                        
#                         ft.ResponsiveRow([
#                             ft.Container(height=50),
#                             # ft.Row([
#                             #     # ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
#                             #     # ft.ElevatedButton("Registro", on_click=showInputs)
#                             # ],
#                             # alignment=ft.MainAxisAlignment.CENTER
#                             # ),
#                             ft.Container(height=50),
#                             ft.Row([
#                                 ft.Image(
#                                     src=f"img/parqueadero.jpeg",
#                                     height=295,
#                                     width=300,
#                                     fit=ft.ImageFit.COVER,
#                                 )
#                             ],
#                             alignment=ft.MainAxisAlignment.CENTER,
#                             )
#                         ],
#                         vertical_alignment=ft.alignment.center
#                         ),
#                     # ]),
#                 ),
#                 # ft.Container(
#                 #     padding=5,
#                 #     col={"sm":6, "md":5, "xl":4},
#                 # ),
#                 # ft.Container(
#                 #     padding=5,
#                 #     col={"sm":0, "md":1, "xl":2},
#                 # )
#             ]
#         )

        
#         # return ft.Column(
#         #     controls=[
#         #         # ft.Column([
#         #         ft.Container(
#         #             alignment=ft.alignment.center,
#         #             content=ft.Stack([
#         #                 ft.Image(
#         #                     src=f"img/fondo.jpg",
#         #                     # width=300,
#         #                     # height=300,
#         #                     fit=ft.ImageFit.COVER
#         #                 ),
#         #                 ft.Row([
#         #                     ft.Column([
#         #                         ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
#         #                         # ft.ElevatedButton("Registro", on_click=showInputs)
#         #                     ])
#         #                 ], 
#         #                 alignment=ft.MainAxisAlignment.CENTER
#         #                 ),
#         #                 # ft.Row([
#         #                     # ft.ElevatedButton("Registro", on_click=lambda _:self.page.go("/register"), icon=ft.icons.EDIT_NOTE),
#         #                     # tblRegistro
#         #                     # card
#         #                 # ]),
#         #                 # card
#         #             ]),
#         #         )
#         #         # ])
#         #     ]
#         # )

# class Home(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#     def build(self):
#         developer_photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

#         return ft.Column([
#             ft.Container(height=100),
#             developer_photo
#         ],
#         horizontal_alignment="center"
#         )

def Home(page):
    developer_photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

    # return ft.Column([
    #     btn_home,
    #     btn_users,
    #     ft.Container(height=100),
    #     developer_photo
    # ],
    # horizontal_alignment="center"
    # )

    if settings.tipo_app == 0:
        # body=ft.Column(
        #     controls=[
        #         ft.Container(height=20),
        #         ft.Container(
        #             alignment=ft.alignment.center,
        #             content=ft.Stack([
        #                 ft.Row([
        #                     ft.Column([
        #                         btn_home,
        #                         btn_users,
        #                     ], expand=2),
        #                     ft.Column([
        #                         ft.Container(height=100),
        #                         developer_photo
        #                     ], expand=10),
        #                 ], 
        #                 alignment=ft.MainAxisAlignment.CENTER,
        #                 ),
        #             ]),
        #         ),
        #         ft.Container(height=50),
        #     ]
        # )

        body=ft.Column([
            ft.Container(height=100),
            developer_photo
        ],
        horizontal_alignment="center"
        )
    else:
        btn_home=ft.FilledButton("Inicio".ljust(21, " "), icon=ft.icons.HOME, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/"))
        btn_users=ft.FilledButton("Usuarios".ljust(18, " "), icon=ft.icons.PERSON_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/users"))
        btn_settings=ft.FilledButton("Configuración", icon=ft.icons.SETTINGS, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/configuration"))
        btn_variables=ft.FilledButton("Variables".ljust(18, " "), icon=ft.icons.FACT_CHECK, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/variables"))
        btn_register=ft.FilledButton("Registro".ljust(18, " "), icon=ft.icons.EDIT_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/register"))
        btn_cash_register=ft.FilledButton("Cuadre de caja", icon=ft.icons.ATTACH_MONEY_SHARP, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/cash_register"))
        btn_closing_day=ft.FilledButton("Cierre de día".ljust(18, " "), icon=ft.icons.CALENDAR_MONTH, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/closing_day"))
        btn_developer=ft.FilledButton("Desarrollador".ljust(16, " "), icon=ft.icons.CODE_ROUNDED, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/developer"))
        btn_logout=ft.FilledButton("Cerrar sesión".ljust(16, " "), icon=ft.icons.POWER_SETTINGS_NEW, icon_color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, style=ft.ButtonStyle(color={
                    ft.ControlState.HOVERED: ft.colors.BLUE_900,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.WHITE,
                }, bgcolor={
                    ft.ControlState.HOVERED: ft.colors.BLUE_50,
                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                    ft.ControlState.DEFAULT: ft.colors.TRANSPARENT,
                }), on_click=lambda _: page.go("/login"))
                
        body=ft.Column(
            controls=[
                ft.Row([
                    ft.Container(
                        height=938,
                        width=200,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=15,
                            color=ft.colors.BLUE_GREY_300,
                            offset=ft.Offset(0, 0),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ),
                        # expand=2,
                        padding=ft.padding.only(0, 20, 0, 0),
                        bgcolor=ft.colors.BLUE_900,
                        border_radius=ft.border_radius.all(10),
                        # alignment=ft.alignment.center,
                        content=ft.Column([
                            # btn_profile,
                            ft.Container(
                                padding=ft.padding.only(10, 10, 10, 10),
                                on_click=lambda e: settings.page.go("/profile"),
                                content=ft.Row([
                                    settings.user_avatar,
                                    # settings.page.user_auth
                                ]),
                            ),
                            ft.Divider(thickness=2),
                            btn_home,
                            btn_users,
                            btn_settings,
                            btn_variables,
                            btn_register,
                            btn_cash_register,
                            btn_closing_day,
                            ft.Divider(thickness=2),
                            btn_developer,
                            ft.Divider(thickness=2),
                            btn_logout
                        ],
                        horizontal_alignment="center",
                        ),
                    ),
                    ft.Container(
                        expand=10,
                        padding=ft.padding.only(0, 20, 0, 0),
                        # bgcolor="blue",
                        content=ft.Column([
                            ft.Container(height=100),
                            developer_photo,
                            ft.Container(height=100),
                        ], 
                        horizontal_alignment="center",
                        ),
                    )
                ]),
            ]
        )

    return body