from flask import Blueprint, render_template
from models.bd import mysql

sugerencias_bp = Blueprint('sugerencias', __name__)

@sugerencias_bp.route('/ver-sugerencias', methods=['GET'])
def verSugerencias():
    conexion = mysql.connection.cursor()
    conexion.execute('SELECT * FROM sugerencias WHERE estado = "en revision"')
    sugerencias = conexion.fetchall()
    return render_template('verSugerencias.html', sugerencias=sugerencias)