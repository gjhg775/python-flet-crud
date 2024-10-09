import flet as ft
from flet import icons
import settings
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

def Login(page):
    lbl_login=ft.Text("Iniciar sesión", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM, width=300, text_align="center", color=ft.colors.PRIMARY)
    user=ft.TextField(width=280, height=60, hint_text="Usuario ó correo electrónico", border="underline", prefix_icon=ft.icons.PERSON_SHARP)
    email=ft.TextField(width=280, height=60, hint_text="Correo electrónico", border="underline", prefix_icon=ft.icons.EMAIL, visible=False)
    password=ft.TextField(width=280, height=60, hint_text="Contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True)
    confirm_password=ft.TextField(width=280, height=60, hint_text="Confirmar contraseña", border="underline", prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, visible=False)
    name=ft.TextField(width=280, height=60, hint_text="Nombre", border="underline", prefix_icon=ft.icons.PERSON_SHARP, visible=False)
    btn_login=ft.ElevatedButton(text="Iniciar sesión", width=280, bgcolor=ft.colors.BLUE_900, color="white")
    btn_reset_password=ft.TextButton("¿Olvidó su contraseña?", visible=True if settings.tipo_app == 1 else False)
    lbl_cuenta=ft.Text("¿No tiene una cuenta?")
    btn_cuenta=ft.TextButton("Crear cuenta")
    btn_loginme=ft.TextButton("Iniciar sesión", visible=False)

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