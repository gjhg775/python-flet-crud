import flet as ft
from flet import icons
from datatable import selectUser

def validateUser(e):
    if user.value != "" and password.value != "":
        usuario=user.value
        contrasena=password.value
        selectUser(usuario, contrasena)
        # page.go("/register")
    else:
        user.focus()

user=ft.TextField(
    width=280,
    height=40,
    hint_text="Usuario",
    border="underline",
    color="black",
    prefix_icon=ft.icons.PERSON_SHARP
)

password=ft.TextField(
    width=280,
    height=40,
    hint_text="Contraseña",
    border="underline",
    color="black",
    prefix_icon=ft.icons.LOCK,
    password=True
)

class Login(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

    def build(self):
        return ft.Column(
            controls=[        
                ft.Container(
                    ft.Column([
                        ft.Container(
                            ft.Text(
                                "Iniciar sesión",
                                width=320,
                                size=30,
                                text_align="center",
                                weight="W900",
                                color="white"
                            ),
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
                            ft.ElevatedButton(
                                text="Iniciar sesión",
                                width=280,
                                bgcolor="black",
                                color="white",
                                on_click=validateUser
                            ),
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
                    height=500,
                    gradient=ft.LinearGradient([
                        ft.colors.PURPLE,
                        ft.colors.PINK,
                        ft.colors.RED
                    ])
                )
            ]
        )





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