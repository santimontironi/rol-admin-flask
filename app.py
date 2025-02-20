import os
import sys
import threading
from flask import Flask, render_template
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from models.bd import inicializar_bd
from routes.registoEmpleados import registroEmpleados_bp
from routes.listadoEmpleados import empleados_bp
from routes.noticias import noticias_bp
from routes.sugerencias import sugerencias_bp

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = "claveSecreta"

# Inicializar base de datos
mysql = inicializar_bd(app)

# Registrar los blueprints
app.register_blueprint(registroEmpleados_bp)
app.register_blueprint(empleados_bp)
app.register_blueprint(noticias_bp)
app.register_blueprint(sugerencias_bp)

@app.route('/')
def inicio():
    return render_template('administrador.html')

def run_flask():
    app.run(debug=False, use_reloader=False, threaded=True)

def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    qt_app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setWindowTitle("Sistema de empleados")
    main_window.showMaximized()

    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    layout.setContentsMargins(0, 0, 0, 0)

    browser = QWebEngineView()
    browser.setUrl(QUrl("http://127.0.0.1:5000/"))
    layout.addWidget(browser)

    main_window.show()
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    main()