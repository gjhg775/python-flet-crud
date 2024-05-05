import time
import locale
import flet as ft
# from flet import Page
# from app import page
from datatable import tblRegistro, tb, get_configuration, get_variables, selectRegisters, selectRegister
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

locale.setlocale(locale.LC_ALL, "")

vlr_total=0
vlr_total=locale.currency(vlr_total, grouping=True)

parqueadero, regimen=get_configuration()

def showInputs(e):
    variables=get_variables()
    if variables != None:
        card.offset=ft.transform.Offset(0,0)
        placa.focus()
        # page.update()
    else:
        title="Variables"
        message=f"Debe ingresar los valores de las variables"
        open_dlg_modal(e, title, message)
        return False

class Register(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Stack([
                        ft.Row([
                            ft.Column([
                                ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
                                # ft.ElevatedButton("Registro", on_click=showInputs)
                            ])
                        ], 
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        # ft.ElevatedButton("Inicio", on_click=lambda _:self.page.go("/"), icon=ft.icons.HOME),
                        # ft.Row([
                        #     tblRegistro,
                        #     card
                        # ]),
                        # ft.ResponsiveRow([
                        #     ft.Column(col=6, controls=[tblRegistro]),
                        #     ft.Column(col=6, controls=[rdbVehiculo, placa, total])
                        # ]),
                    ]),
                ),
                ft.Container(
                    # bgcolor=ft.colors.PRIMARY_CONTAINER,
                    # border_radius=10,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(10, 20, 10, 0),
                    content=ft.Stack([
                       ft.ResponsiveRow([
                            ft.Column(col=6, controls=[tblRegistro]),
                            ft.Column(col=6, controls=[rdbVehiculo, placa, total])
                        ]),
                    ]),
                )
            ]
            # ft.Container(
            #     ft.Column([
            #         ft.Container(
            #             alignment=ft.alignment.center,
            #             content=ft.Stack([
            #                 ft.Image(
            #                     src=f"img/fondo.jpg",
            #                     # width=300,
            #                     # height=300,
            #                     fit=ft.ImageFit.COVER
            #                 ),
            #                 ft.Row([
            #                     ft.Column([
            #                         ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold"),
            #                         # ft.ElevatedButton("Registro", on_click=showInputs)
            #                         ft.ElevatedButton("Registro")
            #                     ])
            #                 ], 
            #                 alignment=ft.MainAxisAlignment.CENTER
            #                 ),
            #                 # ft.Row([
            #                     # ft.ElevatedButton("Registro", on_click=showInputs),
            #                     # tblRegistro
            #                     # card
            #                 # ]),
            #                 # card
            #             ]),
            #         )
            #     ])
            # )
        )

def hideInputs(e):
    card.offset=ft.transform.Offset(2,0)
    # page.update()

def register(e):
    if placa.value != "":
        if rdbVehiculo.value == "Moto":
            if len(placa.value) < 5 or len(placa.value) > 6:
                title="Placa inválida"
                message=f"La placa {placa.value} no es válida para una moto"
                open_dlg_modal(e, title, message)
                return False
            if len(placa.value) == 6 and placa.value[-1] in "0123456789":
                title="Placa inválida"
                message=f"La placa {placa.value} no es válida para una moto"
                open_dlg_modal(e, title, message)
                return False
        if rdbVehiculo.value == "Carro":
            if len(placa.value) != 6 or placa.value[-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                title="Placa inválida"
                message=f"La placa {placa.value} no es válida para un carro"
                open_dlg_modal(e, title, message)
                return False
        for i in placa.value:
            if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if rdbVehiculo.value == "Moto" or rdbVehiculo.value == "Carro":
                    if rdbVehiculo.value == "Moto":
                        message=f"El caracter {i} no es válido para la placa de una moto"
                    if rdbVehiculo.value == "Carro":
                        message=f"El caracter {i} no es válido para la placa de un carro"
                    title="Placa inválida"
                    open_dlg_modal(e, title, message)
                    return False
        vlr_total=selectRegister(rdbVehiculo.value, placa.value)

        if vlr_total == None:
            vlr_total = 0

        if vlr_total == 0:
            message="Registro creado satisfactoriamente"
        else:
            message="Registro actualizado satisfactoriamente"

        placa.value=""
        vlr_total=locale.currency(vlr_total, grouping=True)
        total.hint_text="Total "+str(vlr_total)
        # card.update()
        total.update()
        placa.focus()
        tb.rows.clear()
        selectRegisters()
        tb.update()
        tblRegistro.update()

        # page.snack_bar=ft.SnackBar(
        #     ft.Text(message, color="white"),
        #     bgcolor="green"
        # )
        # page.snack_bar.open=True
        # page.update()

        time.sleep(4)

        vlr_total=0
        vlr_total=locale.currency(vlr_total, grouping=True)
        total.hint_text="Total "+str(vlr_total)
        # card.update()
        total.update()

def close_dlg(e):
    dlg_modal.open=False
    # page.update()
    total.update()

def open_dlg_modal(e, title, message):
    dlg_modal.title=ft.Text(title, text_align="center")
    dlg_modal.content=ft.Text(message, text_align="center")
    # page.dialog=dlg_modal
    dlg_modal.open=True
    # page.update()

def radiogroup_changed(e):
    placa.focus()

rdbVehiculo=ft.RadioGroup(
    content=ft.Row([
        # ft.Text("Vehículo", size=20),
        ft.Radio(label="Moto", value="Moto"),
        ft.Radio(label="Carro", value="Carro"),
        ft.Radio(label="Otro", value="Otro")
    ]),
    value="Moto",
    on_change=radiogroup_changed
)

dlg_modal=ft.AlertDialog(
    bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
    modal=True,
    icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
    # title=ft.Text(title, text_align="center"),
    # content=ft.Text(message, text_align="center"),
    actions=[
        ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg)
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    on_dismiss=lambda e: placa.focus(),
)

placa=ft.TextField(hint_text="Placa", border="underline", text_size=90, width=600, text_align="center", capitalization="CHARACTERS", on_blur=register)
total=ft.TextField(hint_text="Total "+str(vlr_total), border="none", text_size=65, width=600, text_align="right", read_only=True)

card=ft.Card(
    margin=ft.margin.only(0, 50, 0, 0),
    offset=ft.transform.Offset(2,0),
    animate_offset=ft.animation.Animation(300, curve="easeIn"),
    elevation=30,
    content=ft.Container(
        ft.Column([
            ft.Row([
                # ft.Text("Registro", size=20, weight="bold"),
                ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.IconButton(
                    icon="close",
                    icon_size=30,
                    on_click=hideInputs
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            # ft.Row([
            #     ft.Column([
            #         rdbVehiculo,
            #         placa,
            #         total
            #     ])
            # ],
            # alignment=ft.MainAxisAlignment.CENTER
            # # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            # # spacing=20
            # ),
            # ft.Row([
            #     tblRegistro
            #     # lv
            # ],
            # height=268,
            # alignment=ft.MainAxisAlignment.CENTER,
            
            # # spacing=20
            # ),

            ft.ResponsiveRow([
                # ft.Column(col=6, controls=[tblRegistro]),
                ft.Column(col=6, controls=[rdbVehiculo, placa, total])
            ]),

            # ft.Row([
            #     ft.Column([
            #     ft.Text("", size=20, width=530),
            #     ]),
            #     ft.Column([
            #         placa
            #     ]),
            # ],
            # alignment=ft.MainAxisAlignment.END
            # ),
            # ft.Row([
            #     total
            # ],
            # alignment=ft.MainAxisAlignment.END
            # ),
        ]),
        padding=ft.padding.all(10)
    )
)

selectRegisters()





# import time
# import locale
# import flet as ft
# from flet import Page
# from datatable import tblRegistro, tb, get_configuration, get_variables, selectRegisters, selectRegister
# import sqlite3

# conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

# locale.setlocale(locale.LC_ALL, "")

# class Register:

#     # def __init__(self):

#     def main(page:Page):
#         # page.scroll="auto"

#         vlr_total=0
#         vlr_total=locale.currency(vlr_total, grouping=True)

#         parqueadero, regimen=get_configuration()

#         def showInputs(e):
#             variables=get_variables()
#             if variables != None:
#                 card.offset=ft.transform.Offset(0,0)
#                 placa.focus()
#                 page.update()
#             else:
#                 title="Variables"
#                 message=f"Debe ingresar los valores de las variables"
#                 open_dlg_modal(e, title, message)
#                 return False

#         def hideInputs(e):
#             card.offset=ft.transform.Offset(2,0)
#             page.update()

#         def register(e):
#             if placa.value != "":
#                 if rdbVehiculo.value == "Moto":
#                     if len(placa.value) < 5 or len(placa.value) > 6:
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para una moto"
#                         open_dlg_modal(e, title, message)
#                         return False
#                     if len(placa.value) == 6 and placa.value[-1] in "0123456789":
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para una moto"
#                         open_dlg_modal(e, title, message)
#                         return False
#                 if rdbVehiculo.value == "Carro":
#                     if len(placa.value) != 6 or placa.value[-1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                         title="Placa inválida"
#                         message=f"La placa {placa.value} no es válida para un carro"
#                         open_dlg_modal(e, title, message)
#                         return False
#                 for i in placa.value:
#                     if i not in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
#                         if rdbVehiculo.value == "Moto" or rdbVehiculo.value == "Carro":
#                             if rdbVehiculo.value == "Moto":
#                                 message=f"El caracter {i} no es válido para la placa de una moto"
#                             if rdbVehiculo.value == "Carro":
#                                 message=f"El caracter {i} no es válido para la placa de un carro"
#                             title="Placa inválida"
#                             open_dlg_modal(e, title, message)
#                             return False
#                 vlr_total=selectRegister(rdbVehiculo.value, placa.value)

#                 if vlr_total == None:
#                     vlr_total = 0

#                 if vlr_total == 0:
#                     message="Registro creado satisfactoriamente"
#                 else:
#                     message="Registro actualizado satisfactoriamente"

#                 placa.value=""
#                 vlr_total=locale.currency(vlr_total, grouping=True)
#                 total.hint_text="Total "+str(vlr_total)
#                 card.update()
#                 placa.focus()
#                 tb.rows.clear()
#                 selectRegisters()
#                 tb.update()

#                 page.snack_bar=ft.SnackBar(
#                     ft.Text(message, color="white"),
#                     bgcolor="green"
#                 )
#                 page.snack_bar.open=True
#                 page.update()

#                 time.sleep(4)

#                 vlr_total=0
#                 vlr_total=locale.currency(vlr_total, grouping=True)
#                 total.hint_text="Total "+str(vlr_total)
#                 card.update()

#         def close_dlg(e):
#             dlg_modal.open=False
#             page.update()

#         def open_dlg_modal(e, title, message):
#             dlg_modal.title=ft.Text(title, text_align="center")
#             dlg_modal.content=ft.Text(message, text_align="center")
#             page.dialog=dlg_modal
#             dlg_modal.open=True
#             page.update()

#         def radiogroup_changed(e):
#             placa.focus()

#         rdbVehiculo=ft.RadioGroup(
#             content=ft.Row([
#                 # ft.Text("Vehículo", size=20),
#                 ft.Radio(label="Moto", value="Moto"),
#                 ft.Radio(label="Carro", value="Carro"),
#                 ft.Radio(label="Otro", value="Otro")
#             ]),
#             value="Moto",
#             on_change=radiogroup_changed
#         )

#         dlg_modal=ft.AlertDialog(
#             bgcolor=ft.colors.with_opacity(opacity=0.8, color=ft.colors.BLUE_100),
#             modal=True,
#             icon=ft.Icon(name=ft.icons.WARNING_ROUNDED, color=ft.colors.with_opacity(opacity=0.8, color=ft.colors.ORANGE_900), size=50),
#             # title=ft.Text(title, text_align="center"),
#             # content=ft.Text(message, text_align="center"),
#             actions=[
#                 ft.TextButton("Aceptar", autofocus=True, on_click=close_dlg)
#             ],
#             actions_alignment=ft.MainAxisAlignment.END,
#             on_dismiss=lambda e: placa.focus(),
#         )
        
#         placa=ft.TextField(hint_text="Placa", border="underline", text_size=90, width=600, text_align="center", capitalization="CHARACTERS", on_blur=register)
#         total=ft.TextField(hint_text="Total "+str(vlr_total), border="none", text_size=65, width=600, text_align="right", read_only=True)

#         card=ft.Card(
#             margin=ft.margin.only(0, 50, 0, 0),
#             offset=ft.transform.Offset(2,0),
#             animate_offset=ft.animation.Animation(300, curve="easeIn"),
#             elevation=30,
#             content=ft.Container(
#                 ft.Column([
#                     ft.Row([
#                         # ft.Text("Registro", size=20, weight="bold"),
#                         ft.Text("Registro", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
#                         ft.IconButton(
#                             icon="close",
#                             icon_size=30,
#                             on_click=hideInputs
#                         ),
#                     ],
#                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#                     ),
#                     # ft.Row([
#                     #     ft.Column([
#                     #         rdbVehiculo,
#                     #         placa,
#                     #         total
#                     #     ])
#                     # ],
#                     # alignment=ft.MainAxisAlignment.CENTER
#                     # # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
#                     # # spacing=20
#                     # ),
#                     # ft.Row([
#                     #     tblRegistro
#                     #     # lv
#                     # ],
#                     # height=268,
#                     # alignment=ft.MainAxisAlignment.CENTER,
                    
#                     # # spacing=20
#                     # ),

#                     ft.ResponsiveRow([
#                         ft.Column(col=6, controls=[tblRegistro]),
#                         ft.Column(col=6, controls=[rdbVehiculo, placa, total])
#                     ]),

#                     # ft.Row([
#                     #     ft.Column([
#                     #     ft.Text("", size=20, width=530),
#                     #     ]),
#                     #     ft.Column([
#                     #         placa
#                     #     ]),
#                     # ],
#                     # alignment=ft.MainAxisAlignment.END
#                     # ),
#                     # ft.Row([
#                     #     total
#                     # ],
#                     # alignment=ft.MainAxisAlignment.END
#                     # ),
#                 ]),
#                 padding=ft.padding.all(10)
#             )
#         )

#         container=ft.Container(
#             ft.Column([
#                 ft.Container(
#                     alignment=ft.alignment.center,
#                     content=ft.Stack([
#                         ft.Image(
#                             src=f"img/fondo.jpg",
#                             # width=300,
#                             # height=300,
#                             fit=ft.ImageFit.COVER
#                         ),
#                         ft.Row([
#                             ft.Column([
#                                 ft.Text(parqueadero, color=ft.colors.BLUE_900, size=28, weight="bold")
#                                 # ft.ElevatedButton("Registro", on_click=showInputs)
#                             ])
#                         ], 
#                         alignment=ft.MainAxisAlignment.CENTER
#                         ),
#                         # ft.Row([
#                             ft.ElevatedButton("Registro", on_click=showInputs),
#                             # tblRegistro
#                             card
#                         # ]),
#                         # card
#                     ]),
#                 )
#             ])
#         )

#         page.window_always_on_top=True
#         page.window_maximizable=False
#         page.window_resizable=False
#         # page.window_height=600
#         # page.window_width=800
#         # page.window_center()
#         # page.window_bgcolor=ft.colors.TRANSPARENT
#         page.window_opacity=0.8
#         # page.bgcolor=ft.colors.TRANSPARENT
#         page.opacity=0.0
#         page.title="Parqueadero"
#         # page.window_maximized=True
#         page.vertical_alignment="center"
#         page.horizontal_alignment="center"
#         page.add(container)
#         page.update()

#         showInputs
#         selectRegisters()
#         tblRegistro.scroll="auto"
#         tblRegistro.update()
        
#     # ft.app(target=main)
#     # ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=9000)