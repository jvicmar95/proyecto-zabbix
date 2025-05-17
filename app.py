from flask import Flask, render_template_string, request, redirect, send_from_directory
import os

app = Flask(__name__)
tareas = []

# Cargar el HTML desde el archivo
def cargar_html():
    with open('web/index.html', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    html = cargar_html()
    return render_template_string(html, tareas=tareas)

@app.route('/add', methods=['POST'])
def add():
    tarea = request.form.get('tarea')
    if tarea:
        tareas.append(tarea)
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    if 0 <= index < len(tareas):
        tareas.pop(index)
    return redirect('/')

@app.route('/styles.css')
def css():
    return send_from_directory('web', 'styles.css')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
