### EXOSKY

Este proyecto es una aplicación completa que combina un **backend** en **Django** con una base de datos **MySQL** y un **frontend** desarrollado en **Unity** y exportado a **WebGL**.

### Estructura del Proyecto

La estructura de archivos es la siguiente:

* **backend:** Contiene el código fuente de la aplicación Django.
* **db:** Contiene los scripts de configuración de la base de datos MySQL.
* **frontend:** Contiene el proyecto Unity y el resultado de la exportación a WebGL.
* **docker-compose.yml:** Define los servicios de Docker y las configuraciones necesarias para ejecutar el proyecto completo.

### Ejecutando el Proyecto

Para ejecutar la aplicación de forma local, necesitarás tener **Docker Compose** instalado.

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Marioxuloh/exosky.git
   ```
2. **Accede al directorio del proyecto:**
   ```bash
   cd tu-proyecto
   ```
3. **Inicia la aplicación:**
   ```bash
   docker-compose up --build
   ```
   Este comando construirá las imágenes de Docker, creará los contenedores y los iniciará.

### Próximos Pasos

* **Probar la aplicacion web:** Se despliega en la direccion http://localhost:8080 
* **Explora el código:** Profundiza en el código de cada parte del proyecto.