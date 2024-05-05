import flet as ft
from pages.home import Home
from pages.login import Login
from pages.register import Register

def views_handler(page):
    return {
        "/":ft.View(
            route="/",
            controls=[
                Home(page)
            ]
        ),
        "/login":ft.View(
            route="/login",
            controls=[
                Login(page)
            ]
        ),
        "/register":ft.View(
            route="/register",
            controls=[
                Register(page)
            ]
        ),
    }