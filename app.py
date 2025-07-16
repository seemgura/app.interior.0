from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta de opiniones
@app.route("/opinion", methods=["GET", "POST"])
def opinion():
    if request.method == "POST":
        nombre = request.form["nombre"]
        contenido = request.form["contenido"]
        conn = sqlite3.connect("interiorismo.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO opiniones (nombre, contenido) VALUES (?, ?)", (nombre, contenido))
        conn.commit()
        conn.close()
        return redirect("/opinion")
    else:
        conn = sqlite3.connect("interiorismo.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, contenido FROM opiniones")
        opiniones = cursor.fetchall()
        conn.close()
        return render_template("opinion.html", opiniones=opiniones)

if __name__ == "__main__":
    app.run(debug=True)
