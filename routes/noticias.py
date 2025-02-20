from flask import Blueprint, render_template, request,redirect,url_for
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
        rutaImagen = os.path.join('../empleados/static/uploads', nombre_seguro_imagen)
        imagenNoticia.save(rutaImagen)

        conexion = mysql.connection.cursor()
        conexion.execute('INSERT INTO noticias(titulo,descripcion,imagen) VALUES(%s,%s,%s)', (tituloNoticia, descripcionNoticia, nombre_seguro_imagen))
        mysql.connection.commit()
        
        return redirect(url_for('noticias.agregar_noticias'))

    else:
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM noticias WHERE estado = "publicada"')
        noticias = conexion.fetchall()
    
        return render_template('agregar-noticias.html', noticias=noticias)

@noticias_bp.route('/eliminar-noticia',methods=['GET','POST'])
def eliminar_noticia():
    if request.method == "POST":
        idNoticia = request.form['noticiaId']
        conexion = mysql.connection.cursor()
        conexion.execute('UPDATE noticias SET estado = "eliminada" WHERE id_noticia = %s',(idNoticia,))
        mysql.connection.commit()
        return redirect(url_for('noticias.agregar_noticias'))