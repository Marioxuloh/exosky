## **EXOSKY**

This project is a full-stack application combining a **Django** backend with a **MySQL** database and a **Unity** frontend exported to **WebGL**.

### **Project Structure**

The file structure is as follows:

* **backend:** Contains the Django application source code.
* **db:** Contains the MySQL database configuration scripts.
* **frontend:** Contains the Unity project and the result of the export to WebGL.
* **docker-compose.yml:** Defines the Docker services and the necessary configurations to run the entire project.

### **Running the Project**

To run the application locally, you'll need to have **Docker Compose** installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Marioxuloh/exosky.git
   ```
2. **Access the project directory:**
   ```bash
   cd exosky
   ```
3. **Start the application:**
   ```bash
   docker-compose up --build
   ```
   This command will build the Docker images, create the containers, and start them.

4. **Initialize the application:**
   ```bash
   curl -X GET http://localhost:8000/exoplanets/getallandsave/
   ```
   This command will save the exoplanet data to the database to avoid making many calls to the Exoplanet Archive (which is slow).

### **Next Steps**

* **Test the web application:** It's deployed at http://localhost:8082
* **Explore the code:** Delve deeper into the code of each part of the project.

## **Technical Breakdown**

### **Backend (Django)**
* **Purpose:** Handles server-side logic, database interactions, and API endpoints.
* **Technologies:** Python, Django, MySQL
* **Functionality:**
  * Provides a REST API for the frontend to fetch exoplanet data.
  * Manages the MySQL database, storing information about exoplanets.
  * Implements authentication and authorization if necessary.

### **Frontend (Unity/WebGL)**
* **Purpose:** Creates the user interface and provides interactive elements.
* **Technologies:** Unity, C#, WebGL
* **Functionality:**
  * Displays exoplanet data in a visually appealing manner.
  * Allows users to interact with the data, such as filtering or sorting.
  * Handles real-time updates if required.

### **Docker**
* **Purpose:** Packages the application into containers for easy deployment and scaling.
* **Technologies:** Docker, Docker Compose
* **Functionality:**
  * Defines the services (backend, frontend, database) and their dependencies.
  * Manages the lifecycle of the containers, from creation to termination.

### EXOSKY ESPANOL

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
   cd exosky
   ```
3. **Inicia la aplicación:**
   ```bash
   docker-compose up --build
   ```
   Este comando construirá las imágenes de Docker, creará los contenedores y los iniciará.

4. **Inicia la aplicación:**
   ```bash
   curl -X GET http://localhost:8000/exoplanets/getallandsave/
   ```
   Este comando guardara los datos de los exoplanetas en base de datos para no tener que hacer muchas llamadas a Exoplanet Archive (es lento)

### Próximos Pasos

* **Probar la aplicacion web:** Se despliega en la direccion http://localhost:8080 
* **Explora el código:** Profundiza en el código de cada parte del proyecto.
