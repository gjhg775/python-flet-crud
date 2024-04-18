import os
import bcrypt
import sqlite3
from dotenv import load_dotenv

load_dotenv()

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

password=os.getenv("psw")
bytes=password.encode('utf-8')
salt=bcrypt.gensalt()
hash=bcrypt.hashpw(bytes, salt)

def create_tables():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        clave TEXT,
        nombre TEXT)
        """)
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS accesos(
        acceso_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        programa TEXT,
        acceso_usuario INTEGER,
        FOREIGN KEY(acceso_usuario) REFERENCES usuarios(usuario_id))
        """)
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS administracion(
        administracion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        parqueadero TEXT,
        nit TEXT,
        regimen TEXT,
        direccion TEXT,
        telefono TEXT,
        servicio TEXT)
        """)
    conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS registro(
        registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        entrada DATETIME,
        salida DATETIME)
        """)
    conn.commit()

def develop_user():
    try:
        sql="""INSERT INTO usuarios (usuario, clave, nombre) VALUES (?, ?, ?)"""
        values=("Gareca", f"{hash}", "Gabriel Jaime Hoyos Garcés")

        cursor=conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def develop_access():
    try:
        programs=["Registro", "Cuadre", "Cierre", "Variables", "Administración"]

        for x in programs:
            sql=f"""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES (?, ?, ?)"""
            values=("Gareca", f"{x}", 1)

            cursor=conn.cursor()
            cursor.execute(sql, values)
            conn.commit()
    except Exception as e:
        print(e)

create_tables()
develop_user()
develop_access()