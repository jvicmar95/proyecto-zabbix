from flask import Flask, render_template_string, request, redirect, send_from_directory
from db import init_db, obtener_tareas, agregar_tarea, eliminar_tarea

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    with open('web/index.html', encoding='utf-8') as f:
        html = f.read()
    tareas = obtener_tareas()
    return render_template_string(html, tareas=tareas)

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

@app.route('/styles.css')
def css():
    return send_from_directory('web', 'styles.css')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
