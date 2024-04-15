import sqlite3
conn=sqlite3.connect("database/parqueadero.db", check_same_thread=False)

def create_tables():
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS registro(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        placa TEXT,
        entrada DATE,
        quantity INTEGER)
        """)
    conn.commit()