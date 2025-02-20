from flask_mysqldb import MySQL

mysql = MySQL()

def inicializar_bd(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_DB'] = 'proyecto'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    return MySQL(app)