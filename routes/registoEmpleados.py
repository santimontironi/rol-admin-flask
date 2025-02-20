from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
import re
from models.bd import mysql

registroEmpleados_bp = Blueprint('auth', __name__)
 
@registroEmpleados_bp.route('/registro-empleado', methods=["GET", "POST"])
def registro():
    nuevoRegistro, yaRegistrado = None, None

    if request.method == "POST":
        nombre = request.form['nombre_registro']
        apellido = request.form['apellido_registro']
        correo = request.form['correo_registro']
        clave = request.form['clave_registro']

        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', clave):
            errorClave = "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número."
            return render_template('registroempleados.html', errorClave=errorClave)

        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM registroempleados WHERE correo_registro = %s', (correo,))
        
        if conexion.fetchone():
            yaRegistrado = "Este empleado ya existe. Vuelva a intentarlo."
        else:
            hashed_password = generate_password_hash(clave)
            conexion.execute('INSERT INTO registroempleados (nombre, apellido, correo_registro, clave_registro) VALUES (%s, %s, %s, %s)', (nombre, apellido, correo, hashed_password))
            mysql.connection.commit()
            nuevoRegistro = "Usuario creado exitosamente!"

    return render_template('registroempleados.html', yaRegistrado=yaRegistrado, nuevoRegistro=nuevoRegistro)

