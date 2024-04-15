import flet as ft
from flet import Icon

container = ft.Container(
    ft.Column([
        ft.Container(
            ft.Text(
                value="Registro",
                size=30,
                weight="w100",
                text_align="left"
            ),
            ft.ElevatedButton("Nuevo")
        )
    ])
)

def main(page: ft.Page):
    # page.vertical_alignment="center"
    # page.horizontal_alignment="center"
    page.add(container)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9000)