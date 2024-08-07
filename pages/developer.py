import flet as ft

# class Developer(ft.UserControl):
#     def __init__(self, page):
#         super().__init__()
#         self.page=page

#     def build(self):
#         developer_photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
#         developer_name=ft.Text("Desarrollado por Gareca", theme_style=ft.TextThemeStyle.TITLE_LARGE)
#         copyright=ft.Text("Copyright © 2024", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
#         rights=ft.Text("Todos los derechos reservados", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)

#         return ft.Column([
#             ft.Container(height=100),
#             developer_photo,
#             # ft.Container(height=20),
#             developer_name,
#             copyright,
#             rights
#         ],
#         horizontal_alignment="center"
#         )

def Developer(page):
    page.scroll="auto"
    
    # developer_photo=ft.Image(src=f"img/parqueadero.jpeg", height=296, width=300, fit=ft.ImageFit.COVER, border_radius=150)
    developer_photo=ft.Icon(name=ft.icons.PERSON, color=ft.colors.PRIMARY_CONTAINER, scale=(10))
    developer_name=ft.Text("Desarrollado por Gareca", theme_style=ft.TextThemeStyle.TITLE_LARGE)
    copyright=ft.Text("Copyright © 2024", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    rights=ft.Text("Derechos reservados", theme_style=ft.TextThemeStyle.TITLE_MEDIUM)

    return ft.Column([
        # ft.Container(height=100),
        ft.Container(height=200),
        developer_photo,
        # ft.Container(height=20),
        ft.Container(height=70),
        developer_name,
        copyright,
        rights,
        ft.Container(height=50),
    ],
    horizontal_alignment="center"
    )