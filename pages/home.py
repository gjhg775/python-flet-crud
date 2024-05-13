# import flet as ft
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

import flet as ft

class Home(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

    def build(self):
        developer_photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)

        return ft.Column([
            ft.Container(height=100),
            developer_photo
        ],
        horizontal_alignment="center"
        )