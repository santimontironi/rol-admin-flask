import os #manejar archivos del sistema operativo.
from models.bd import inicializar_bd
from flask import Flask, request, url_for, render_template, redirect
from werkzeug.utils import secure_filename #libreria para hacer nombres de archivos mas seguros.
from werkzeug.security import generate_password_hash #libreria para el hash de claves.
import re # proporciona herramientas para trabajar con expresiones regulares. Las expresiones regulares son una poderosa herramienta para buscar, comparar y manipular cadenas de texto según patrones específicos.

import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

#SE GENERA UNA CLAVE DE FLASK Y EL ENTORNO DE TRABAJO DE LA APP.
app = Flask(__name__)
app.secret_key = "claveSecreta"

#INICIALIZACION DE LA BD
mysql = inicializar_bd(app)

@app.route('/')
def inicio():
    return render_template('administrador.html')

#RUTA Y FUNCION REGISTRO DE EMPLEADOS
@app.route('/registro-empleado', methods=["GET", "POST"])
def registro():
    nuevoRegistro = None
    yaRegistrado = None
    
    if request.method == "POST":
        nombreRegistro = request.form['nombre_registro']
        apellidoRegistro = request.form['apellido_registro']
        correoRegistro = request.form['correo_registro']
        claveRegistro = request.form['clave_registro']
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', claveRegistro):
            errorClave = "La contraseña debe tener al menos 8 caracteres, incluyendo una mayúscula, una minúscula y un número."
            return render_template('registroempleados.html', errorClave = errorClave)
        
        conexion = mysql.connection.cursor()
        
        conexion.execute('SELECT * FROM registroempleados WHERE correo_registro = %s', (correoRegistro,))
        registro = conexion.fetchone()
        
        if registro:
            yaRegistrado = "Este empleado ya existe. Vuelva a intentarlo."
        else:
            hashed_password = generate_password_hash(claveRegistro)
            
            
            conexion.execute('INSERT INTO registroempleados (nombre, apellido, correo_registro, clave_registro) VALUES (%s, %s, %s, %s)', (nombreRegistro, apellidoRegistro, correoRegistro, hashed_password))
            mysql.connection.commit()
            
            
            nuevoRegistro = "Usuario creado exitosamente!"
            
    return render_template('registroempleados.html', yaRegistrado=yaRegistrado, nuevoRegistro=nuevoRegistro)


#RUTA Y FUNCION PARA EL LISTADO DE EMPLEADOS
@app.route('/listado-empleados',methods=['GET'])
def listadoEmpleados():
    empleados = []
    if request.method == 'GET':
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM registroempleados WHERE estado = "Activo"')
        empleados = conexion.fetchall()
        
    return render_template('listadoEmpleados.html',empleados = empleados)

#RUTA Y FUNCION PARA ELIMINAR EMPLEADOS
@app.route('/eliminar-empleados', methods=['GET','POST'])
def eliminarEmpleados():
    if request.method == "POST":
        conexion = mysql.connection.cursor()
        idEmpleado = request.form['idEmpleado']
        conexion.execute('UPDATE registroempleados SET estado = "Eliminado" WHERE id = %s', (idEmpleado,))
        mysql.connection.commit()
        
    return redirect(url_for('listadoEmpleados'))

#RUTA Y FUNCION PARA AGERGAR NOTICIAS
@app.route('/agregar_noticias', methods=['GET', 'POST'])
def agregar_noticias():
    noticias = []
    if request.method == "POST":
        tituloNoticia = request.form['tituloNoticia']
        descripcionNoticia = request.form['descripcionNoticia']
        imagenNoticia = request.files['imagenNoticia']
        
        nombre_seguro_imagen = secure_filename(imagenNoticia.filename) #convierte la imagen en un nombre seguro
        rutaImagen = os.path.join('..','empleados', 'static', 'uploads',nombre_seguro_imagen) #se establece la ruta del guardado de la imagen
        imagenNoticia.save(rutaImagen) #guarda la imagen en la carpeta uploads
        
        conexion = mysql.connection.cursor()
        
        conexion.execute('INSERT INTO noticias(titulo,descripcion,imagen) VALUES(%s,%s,%s)',(tituloNoticia,descripcionNoticia,nombre_seguro_imagen))
        
        mysql.connection.commit()

    else:
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM noticias WHERE estado = "publicada"')
        noticias = conexion.fetchall()
        return render_template('agregar-noticias.html', noticias = noticias)
    
    return redirect(url_for('agregar_noticias'))

#RUTA Y FUNCION PARA ELIMINAR NOTICIA
@app.route('/eliminar-noticia', methods=['POST'])
def eliminar_noticia():
    if request.method == "POST":
        noticiaId = request.form['noticiaId']
        conexion = mysql.connection.cursor()
        conexion.execute('UPDATE noticias SET estado = "eliminada" WHERE id_noticia = %s',(noticiaId,))
        mysql.connection.commit()
    
    return redirect(url_for('agregar_noticias'))

#RUTA Y FUNCION PARA VER LAS SUGERENCIAS
@app.route('/ver-sugerencias',methods = ['GET','POST'])
def verSugerencias():
    sugerencias = []
    empleado = []
    if request.method == 'GET':
        conexion = mysql.connection.cursor()
        conexion.execute('SELECT * FROM sugerencias WHERE estado = "en revision"')
        sugerencias = conexion.fetchall()
        
        for sugerencia in sugerencias:
            id_empleado = sugerencia['id_empleado']
        
            conexion.execute("SELECT nombre, apellido FROM registroempleados where id = %s",(id_empleado,))
            empleado = conexion.fetchone()
        
    return render_template('verSugerencias.html',sugerencias = sugerencias, empleado = empleado)
        
#RUTA Y FUNCION PARA RESPONDER SUGERENCIA
@app.route('/responder-sugerencia', methods = ['POST','GET'])
def responderSugerencia():
    if request.method == "POST":
        sugerenciaId = request.form['sugerenciaId']
        respuesta = request.form['respuesta']
        
        conexion = mysql.connection.cursor()
        
        conexion.execute('UPDATE sugerencias SET respuesta = %s WHERE id_sugerencia = %s',(respuesta,sugerenciaId))
        mysql.connection.commit()
        
        conexion.execute('UPDATE sugerencias SET estado = "Respondida" WHERE id_sugerencia = %s',(sugerenciaId,))
        mysql.connection.commit()
        
    return redirect(url_for('verSugerencias'))


def run_flask():
    app.run(debug=False, use_reloader=False, threaded=True)


def main():
    # Iniciar Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Asegura que el hilo se cierre al cerrar la app
    flask_thread.start()
    
    # Crear la aplicación PyQt5
    qt_app = QApplication(sys.argv)
    
    # Crear la ventana principal
    main_window = QMainWindow()
    main_window.setWindowTitle("Sistema de empleados")
    main_window.showMaximized()  # Maximiza la ventana
    
    # Crear un contenedor central y el diseño
    central_widget = QWidget() #Crea un contenedor vacío que actuará como el widget central de la ventana.
    main_window.setCentralWidget(central_widget) #Asigna el contenedor como el widget principal de la ventana.
    layout = QVBoxLayout(central_widget) #Crea un diseño vertical dentro del contenedor, para que los elementos se apilen uno debajo del otro.
    layout.setContentsMargins(0, 0, 0, 0)  # Elimina los márgenes alrededor del diseño
    
    # Crear un widget de navegador para mostrar Flask
    browser = QWebEngineView()
    
    # Espera un momento antes de cargar la URL para asegurarse de que Flask esté listo
    browser.setUrl(QUrl("http://127.0.0.1:5000/"))  # Carga la URL del servidor Flask
    layout.addWidget(browser)
    
    # Mostrar la ventana principal
    main_window.show()
    
    # Ejecutar la aplicación GUI
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()