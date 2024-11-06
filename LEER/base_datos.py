import sqlite3


TABLA = 'lecturas'
conexion = sqlite3.connect("lecturas.db")
cursor = conexion.cursor()

cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {TABLA} (
    ID           TEXT    PRIMARY KEY,
    NOMBRE       TEXT    NOT NULL,
    APELLIDO     TEXT    NOT NULL,
    CURSO        INTEGER NOT NULL,
    DIVISION     INTEGER NOT NULL,
    ACOMPANANTES INTEGER NOT NULL,
    VALIDO       INTEGER NOT NULL,
    ESCANEADAS   INTEGER NOT NULL
)
""")

def agregar(datos: dict):
    lista_datos = [datos[key] for key in ['ID',
                                          'NOMBRE',
                                          'APELLIDO',
                                          'CURSO',
                                          'DIVISION',
                                          'ACOMPANANTES',
                                          'VALIDO']]
    print(lista_datos)
    cursor.execute(f'INSERT INTO {TABLA} VALUES (?,?,?,?,?,?,?,?)', tuple(dato for dato in lista_datos))

def mostrar():
    cursor.execute(f'SELECT * FROM {TABLA}')
    usuarios = cursor.fetchall()
    print('Usuarios en la base de datos:', usuarios)
    for usuario in usuarios:
        print(usuario)

conexion.commit()
conexion.close()