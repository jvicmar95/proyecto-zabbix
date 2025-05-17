from flask import Flask, render_template, request, redirect
from db import init_db, obtener_tareas, agregar_tarea, eliminar_tarea

# Inicializa la app y define dónde buscar templates y estáticos
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')

# Creamos la base de datos si no existe
init_db()

@app.route('/')
def index():
    tareas = obtener_tareas()
    return render_template('index.html', tareas=tareas)

@app.route('/add', methods=['POST'])
def add():
    tarea = request.form.get('tarea')
    if tarea:
        agregar_tarea(tarea)
        print(f"✔ Tarea agregada: {tarea}")
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    eliminar_tarea(index)
    print(f"✖ Tarea en índice {index} eliminada")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
