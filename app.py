from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = 'interiorismo.db'

# Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS opiniones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            opinion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, opinion FROM opiniones")
    opiniones = cursor.fetchall()
    conn.close()
    return render_template('index.html', opiniones=opiniones)

@app.route('/opinion', methods=['POST'])
def opinion():
    nombre = request.form['nombre']
    opinion = request.form['opinion']
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO opiniones (nombre, opinion) VALUES (?, ?)", (nombre, opinion))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
