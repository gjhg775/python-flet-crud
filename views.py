import flet as ft
from pages.home import Home
from pages.login import Login
from pages.variables import Variables
from pages.register import Register
from pages.cash_register import Cash_register
from pages.closing_day import Closing_day
from pages.developer import Developer

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
        "/variables":ft.View(
            route="/variables",
            controls=[
                Variables(page)
            ]
        ),
        "/register":ft.View(
            route="/register",
            controls=[
                Register(page)
            ]
        ),
        "/cash_register":ft.View(
            route="/cash_register",
            controls=[
                Cash_register(page)
            ]
        ),
        "/closing_day":ft.View(
            route="/closing_day",
            controls=[
                Closing_day(page)
            ]
        ),
        "/developer":ft.View(
            route="/developer",
            controls=[
                Developer(page)
            ]
        ),
    }