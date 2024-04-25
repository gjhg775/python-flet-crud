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

def create_users():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        clave TEXT,
        nombre TEXT)
        """)
    conn.commit()

def drop_users():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")

def create_access():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS accesos(
        acceso_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        programa TEXT,
        acceso_usuario INTEGER,
        FOREIGN KEY(acceso_usuario) REFERENCES usuarios(usuario_id))
        """)
    conn.commit()

def drop_access():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS accesos")

def create_configuration():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS configuracion(
        administracion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        parqueadero TEXT,
        nit TEXT,
        regimen TEXT,
        direccion TEXT,
        telefono TEXT,
        servicio TEXT,
        consecutivo TEXT)
        """)
    conn.commit()

def drop_configuration():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS configuracion")

def create_variables():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS variables(
        vlr_hora_moto INTEGER,
        vlr_dia_moto INTEGER,
        vlr_hora_carro INTEGER,
        vlr_dia_carro INTEGER,
        vlr_hora_otro INTEGER,
        vlr_dia_otro INTEGER)
        """)
    conn.commit()

def drop_variables():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS variables")

def create_regist():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS registro(
        registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        entrada TEXT,
        salida TEXT,
        vehiculo TEXT,
        valor INTEGER,
        total INTEGER,
        cuadre INTEGER,
        usuario TEXT)
        """)
    conn.commit()

def drop_regist():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS registro")

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

drop_regist()
drop_variables()
drop_configuration()
drop_access()
drop_users()

create_users()
create_access()
create_configuration()
create_variables()
create_regist()
develop_user()
develop_access()

conn.close()