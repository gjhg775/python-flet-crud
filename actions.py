import bcrypt
import sqlite3

conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

password=""
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

create_tables()

cursor=conn.cursor()

cursor.execute(f"""INSERT INTO usuarios (usuario, clave, nombre) VALUES ("Gareca", "{hash}", "Gabriel Jaime Hoyos Garcés")""")
conn.commit()

cursor.execute("""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES ("Gareca", "Registro", 1)""")
conn.commit()
cursor.execute("""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES ("Gareca", "Cuadre", 1)""")
conn.commit()
cursor.execute("""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES ("Gareca", "Cierre", 1)""")
conn.commit()
cursor.execute("""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES ("Gareca", "Variables", 1)""")
conn.commit()
cursor.execute("""INSERT INTO accesos (usuario, programa, acceso_usuario) VALUES ("Gareca", "Administración", 1)""")
conn.commit()