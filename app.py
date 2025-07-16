from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Función para crear la tabla de opiniones si no existe
def init_db():
    with sqlite3.connect('interiorismo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opiniones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                opinion TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route("/", methods=["GET"])
def index():
    conn = sqlite3.connect('interiorismo.db')
    cursor = conn.cursor()

    # Obtener estilos
    cursor.execute("SELECT * FROM estilos")
    estilos = cursor.fetchall()

    # Obtener opiniones
    cursor.execute("SELECT nombre, opinion FROM opiniones ORDER BY id DESC")
    opiniones = cursor.fetchall()

    conn.close()
    return render_template("index.html", estilos=estilos, opiniones=opiniones)

@app.route("/opiniones", methods=["POST"])
def guardar_opinion():
    nombre = request.form["nombre"]
    opinion = request.form["opinion"]

    conn = sqlite3.connect('interiorismo.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO opiniones (nombre, opinion) VALUES (?, ?)", (nombre, opinion))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()  # Asegura que la tabla exista antes de correr
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
