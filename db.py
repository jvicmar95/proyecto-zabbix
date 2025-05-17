import sqlite3
import os

# Usamos /data para guardar tareas.db porque es donde está montado el volumen
DB_FILE = os.path.join('/data', 'tareas.db')

# Crea la tabla si no existe
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tareas (id INTEGER PRIMARY KEY AUTOINCREMENT, texto TEXT)')
    conn.commit()
    conn.close()

# Devuelve todas las tareas en forma de lista de strings
def obtener_tareas():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT texto FROM tareas')
    tareas = [fila[0] for fila in c.fetchall()]
    conn.close()
    return tareas

# Agrega una nueva tarea
def agregar_tarea(texto):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO tareas (texto) VALUES (?)', (texto,))
    conn.commit()
    conn.close()

# Elimina una tarea por su índice (posición)
def eliminar_tarea(indice):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM tareas WHERE rowid IN (SELECT rowid FROM tareas LIMIT 1 OFFSET ?)', (indice,))
    conn.commit()
    conn.close()
