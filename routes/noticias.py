from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
import os
from models.bd import mysql

noticias_bp = Blueprint('noticias', __name__)

@noticias_bp.route('/agregar_noticias', methods=['GET', 'POST'])
def agregar_noticias():
    noticias = []
    if request.method == "POST":
        tituloNoticia = request.form['tituloNoticia']
        descripcionNoticia = request.form['descripcionNoticia']
        imagenNoticia = request.files['imagenNoticia']

        nombre_seguro_imagen = secure_filename(imagenNoticia.filename)
        rutaImagen = os.path.join('static/uploads', nombre_seguro_imagen)
        imagenNoticia.save(rutaImagen)

        conexion = mysql.connection.cursor()
        conexion.execute('INSERT INTO noticias(titulo,descripcion,imagen) VALUES(%s,%s,%s)', (tituloNoticia, descripcionNoticia, nombre_seguro_imagen))
        mysql.connection.commit()

    else:
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM noticias WHERE estado = "publicada"')
        noticias = conexion.fetchall()
    
    return render_template('agregar-noticias.html', noticias=noticias)