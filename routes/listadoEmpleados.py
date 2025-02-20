from flask import Blueprint, render_template
from models.bd import mysql 

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/empleados')
def listar_empleados():
    conexion = mysql.connection.cursor()
    conexion.execute("SELECT * FROM registroempleados")
    empleados = conexion.fetchall()
    return render_template('listadoEmpleados.html', empleados=empleados)
