import flet as ft

class Developer(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

    def build(self):
        Developer_photo=ft.Image(src="img/dev.png", height=130, width=150)
        developer_name=ft.Text("Desarrollado por Gareca", theme_style=ft.TextThemeStyle.TITLE_LARGE, color=ft.colors.BLACK87)
        copyright=ft.Text("Copyright © 2024", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.BLUE_GREY_900)
        rights=ft.Text("Todos los derechos reservados", theme_style=ft.TextThemeStyle.TITLE_MEDIUM, color=ft.colors.BLUE_GREY_900)

        return ft.Column([
            ft.Container(height=100),
            Developer_photo,
            ft.Container(height=20),
            developer_name,
            copyright,
            rights
        ],
        horizontal_alignment="center"
        )