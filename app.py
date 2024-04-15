from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'monorail.proxy.rlwy.net'
DB_NAME = 'railway'
DB_USER = 'postgres'
DB_PASSWORD = 'MDKBYFGerdHPErjmxNGfjEOJqAbqCThI'

def conectar_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)


def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO persona (documento, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                   (dni, nombre, apellido, direccion, telefono))
    conn.commit()
    conn.close()

def obtener_registros():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM persona order by apellido")
    registros = cursor.fetchall()
    conn.close()
    return registros

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    mensaje_confirmacion = "Registro Exitoso"
    return redirect(url_for('index', mensaje_confirmacion=mensaje_confirmacion))

@app.route('/administrar')
def administrar():
    registros=obtener_registros()
    return render_template('administrar.html',registros=registros)

@app.route('/eliminar/<dni>', methods=['POST'])
def eliminar_registro(dni):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor=conn.cursor()
    cursor.execute("DELETE FROM persona WHERE documento = %s", (dni,))
    conn.commit()
    conn.close()
    return redirect(url_for('administrar'))

if __name__ == '__main__':
    app.run(debug=True)
