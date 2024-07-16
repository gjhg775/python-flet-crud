import os
import bcrypt
import sqlite3
import hashlib
from dotenv import load_dotenv

load_dotenv()

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

password=os.getenv("pswsa")
# bytes=password.encode('utf-8')
# hashsa=hashlib.sha256(bytes).hexdigest()
hashsa=password

password=os.getenv("pswa")
# bytes=password.encode('utf-8')
# hasha=hashlib.sha256(bytes).hexdigest()
hasha=password

# # salt=bcrypt.gensalt()
# # hash=bcrypt.hashpw(bytes, salt)

def create_users():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        clave TEXT,
        nombre TEXT,
        foto TEXT)
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
        FOREIGN KEY(acceso_id) REFERENCES usuarios(usuario_id))
        """)
    conn.commit()

def drop_access():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS accesos")

def create_configuration():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS configuracion(
        configuracion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        parqueadero TEXT,
        nit TEXT,
        regimen TEXT,
        direccion TEXT,
        telefono TEXT,
        servicio TEXT,
        consecutivo TEXT,
        vista_previa INTEGER,
        imprimir INTEGER,
        impresora TEXT)
        """)
    conn.commit()

def drop_configuration():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS configuracion")

def create_variables():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS variables(
        variable_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vlr_hora_moto INTEGER,
        vlr_turno_moto INTEGER,
        vlr_hora_carro INTEGER,
        vlr_turno_carro INTEGER,
        vlr_hora_otro INTEGER,
        vlr_turno_otro INTEGER)
        """)
    conn.commit()

def drop_variables():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS variables")

def create_regist():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS registro(
        registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consecutivo TEXT,
        placa TEXT,
        entrada TEXT,
        salida TEXT,
        vehiculo TEXT,
        facturacion INTEGER,
        valor INTEGER,
        tiempo INTEGER,
        total INTEGER,
        cuadre INTEGER,
        ingreso TEXT,
        retiro TEXT)
        """)
    conn.commit()

def drop_regist():
    cursor=conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS registro")

def admin_user():
    try:
        cursor=conn.cursor()
        sql="""INSERT INTO usuarios (usuario, clave, nombre, foto) VALUES (?, ?, ?, ?)"""
        values=("Super Admin", f"{hashsa}", "Super Administrador", "default.jpg")
        cursor.execute(sql, values)
        conn.commit()

        sql="""INSERT INTO usuarios (usuario, clave, nombre, foto) VALUES (?, ?, ?, ?)"""
        values=("Admin", f"{hasha}", "Administrador", "default.jpg")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def admin_access():
    try:
        programs=["Configuración", "Variables", "Registro", "Cuadre", "Cierre"]

        for x in programs:
            cursor=conn.cursor()
            sql=f"""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES (?, ?, ?)"""
            values=("Super Admin", f"{x}", 1)
            cursor.execute(sql, values)
            conn.commit()
        for x in programs:
            cursor=conn.cursor()
            sql=f"""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES (?, ?, ?)"""
            values=("Admin", f"{x}", 1)
            cursor.execute(sql, values)
            conn.commit()
    except Exception as e:
        print(e)

def add_configuration():
    try:
        cursor=conn.cursor()
        sql="""INSERT INTO configuracion (parqueadero, nit, regimen, direccion, telefono, servicio, consecutivo, vista_previa, imprimir, impresora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=("", "", "", "", "", "", "", "1", "1", "")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def add_variables():
    try:
        cursor=conn.cursor()
        sql="""INSERT INTO variables (vlr_hora_moto, vlr_turno_moto, vlr_hora_carro, vlr_turno_carro, vlr_hora_otro, vlr_turno_otro) VALUES (?, ?, ?, ?, ?, ?)"""
        values=("", "", "", "", "", "")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

drop_regist()
# drop_variables()
# drop_configuration()
# drop_access()
# drop_users()

# create_users()
# create_access()
# create_configuration()
# create_variables()
create_regist()
# admin_user()
# admin_access()
# add_configuration()
# add_variables()

conn.close()