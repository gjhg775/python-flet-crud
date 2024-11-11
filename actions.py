import os
import bcrypt
import settings
import sqlite3
import hashlib
from dotenv import load_dotenv

load_dotenv()

# try:
#     conn=sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
# except Exception as e:
#     print(e)

# if settings.tipo_app == 0:
#     conn=sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
# else:
#     conn=sqlite3.connect('FILE C:\\pdb\\data\\parqueadero.db', check_same_thread=False)

password=os.getenv("PSWSA")
# bytes=password.encode('utf-8')
# hashsa=hashlib.sha256(bytes).hexdigest()
hashsa=password

password=os.getenv("PSWA")
# bytes=password.encode('utf-8')
# hasha=hashlib.sha256(bytes).hexdigest()
hasha=password

# # salt=bcrypt.gensalt()
# # hash=bcrypt.hashpw(bytes, salt)

def get_connection():
    try:
        return sqlite3.connect('C:/pdb/data/parqueadero.db', check_same_thread=False)
    except Exception as e:
        print(e)

conn=get_connection()

def create_users():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        correo_electronico TEXT,
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
        facturacion INTEGER,
        resolucion TEXT,
        fecha_desde TEXT,
        fecha_hasta TEXT,
        prefijo TEXT,
        autoriza_del TEXT,
        autoriza_al TEXT,
        clave_tecnica TEXT,
        tipo_ambiente INTEGER,
        cliente INTEGER,
        consecutivo TEXT,
        vista_previa_registro INTEGER,
        imprimir_registro INTEGER,
        enviar_correo_electronico INTEGER,
        email_user TEXT,
        email_pass TEXT,
        vista_previa_cuadre INTEGER,
        imprimir_cuadre INTEGER,
        impresora TEXT,
        papel INTEGER)
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
    try:
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
            retiro TEXT,
            correo_electronico TEXT)
            """)
        conn.commit()
    except Exception as e:
        print(e)

def drop_regist():
    try:
        cursor=conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS registro")
    except Exception as e:
        print(e)

def admin_user():
    try:
        cursor=conn.cursor()
        sql="""INSERT INTO usuarios (usuario, correo_electronico, clave, nombre, foto) VALUES (?, ?, ?, ?, ?)"""
        values=("Super Admin", os.getenv("EMAIL_USER"), f"{hashsa}", "Super Administrador", "default1.jpg")
        cursor.execute(sql, values)
        conn.commit()

        sql="""INSERT INTO usuarios (usuario, correo_electronico, clave, nombre, foto) VALUES (?, ?, ?, ?, ?)"""
        values=("Admin", "", f"{hasha}", "Administrador", "default.jpg")
        cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)

def admin_access():
    try:
        programs=["Usuarios", "Configuración", "Variables", "Registro", "Cuadre", "Cierre"]

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
        sql="""INSERT INTO configuracion (parqueadero, nit, regimen, direccion, telefono, servicio, facturacion, resolucion, fecha_desde, fecha_hasta, prefijo, autoriza_del, autoriza_al, clave_tecnica, tipo_ambiente, cliente, consecutivo, vista_previa_registro, imprimir_registro, enviar_correo_electronico, email_user, email_pass, vista_previa_cuadre, imprimir_cuadre, impresora, papel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values=("", "", "", "", "", "", 0, "", "", "", "", "", "", "", 0, 0, "", 1, 1, 0, "", "", 1, 1, "", 0)
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

try:
    conn.close()
except Exception as e:
        print(e)