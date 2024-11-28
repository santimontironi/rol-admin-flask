# Sistema de administrador de la empresa FullWeb

Este proyecto es una aplicación desarrollada con **Flask** y **PyQt5** que permite gestionar empleados, noticias y sugerencias dentro de una organización, fue realizada para un proyecto final de la universidad, con el fin de aplicar documentación del sistema y buen uso de bases de datos. Combina una interfaz web accesible mediante navegador con una ventana gráfica para facilitar su uso.

## Funcionalidades principales

### Gestión de empleados
- **Registro de empleados:** Permite registrar nuevos empleados con validación de datos y contraseñas seguras.
- **Listado de empleados:** Muestra empleados activos en la base de datos.
- **Eliminación de empleados:** Permite marcar a empleados como "eliminados" sin borrar sus datos de la base.

### Gestión de noticias
- **Agregar noticias:** Opción para subir noticias con título, descripción e imagen.
- **Listado de noticias:** Visualización de las noticias publicadas.
- **Eliminar noticias:** Marca noticias como "eliminadas" en lugar de eliminarlas definitivamente.

### Gestión de sugerencias
- **Visualización de sugerencias:** Muestra las sugerencias enviadas por los empleados.
- **Responder sugerencias:** Permite registrar una respuesta y actualizar el estado de las sugerencias a "Respondida".

## Requisitos previos

1. **Instalar XAMPP**: Asegúrate de tener los servicios de **Apache** y **MySQL** activados.
2. **Configurar la base de datos**:
   - Crea una base de datos en tu gestor preferido (por ejemplo, **MySQL Workbench** o **phpMyAdmin**).
   - Importa el archivo `.sql` incluido en el proyecto (CARPETA MODELS) para crear las tablas necesarias.

3. **Instalar dependencias del proyecto**:
   - Crea un entorno virtual:
     ```bash
     python -m venv .venv
     ```
   - Activa el entorno virtual:
     - En Windows:
       ```bash
       .venv\Scripts\activate
       ```
     - En macOS/Linux:
       ```bash
       source .venv/bin/activate
       ```
   - Instala las dependencias:
     ```bash
     pip install -r requirements.txt
     ```

## Uso de la aplicación

### Ejecución de la aplicación
1. Asegúrate de que los servicios de **Apache** y **MySQL** estén activos.
2. Ejecuta el script principal:
   ```bash
   python app.py

## Tecnologias utilizadas:
1. Flask: Framework backend para manejar rutas y lógica del servidor.
2. PyQt5: Framework para construir la interfaz gráfica de usuario.
3. MySQL: Gestión de la base de datos.
4. Werkzeug: Librerías para hash de contraseñas y seguridad.
5. Bootstrap: Diseño responsivo de la interfaz web.
   
