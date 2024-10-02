#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME="my_mysql_container"
IMAGE_NAME="my_mysql_image"

# Función para crear el contenedor
create() {
    if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
        echo "El contenedor '$CONTAINER_NAME' ya existe."
    else
        echo "Construyendo la imagen '$IMAGE_NAME'..."
        docker build -t $IMAGE_NAME .
        echo "Creando el contenedor '$CONTAINER_NAME'..."
        docker run --name $CONTAINER_NAME -d -p 3306:3306 $IMAGE_NAME
        echo "Contenedor '$CONTAINER_NAME' creado y ejecutándose."
    fi
}

# Función para iniciar el contenedor
start() {
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "El contenedor '$CONTAINER_NAME' ya está en ejecución."
    else
        if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
            echo "Iniciando el contenedor '$CONTAINER_NAME'..."
            docker start $CONTAINER_NAME
            echo "Contenedor '$CONTAINER_NAME' iniciado."
        else
            echo "El contenedor '$CONTAINER_NAME' no existe."
        fi
    fi
}

# Función para parar el contenedor
stop() {
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "Deteniendo el contenedor '$CONTAINER_NAME'..."
        docker stop $CONTAINER_NAME
        echo "Contenedor '$CONTAINER_NAME' detenido."
    else
        echo "El contenedor '$CONTAINER_NAME' no está en ejecución."
    fi
}

# Función para eliminar el contenedor
delete() {
    if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
        echo "Eliminando el contenedor '$CONTAINER_NAME'..."
        docker rm -f $CONTAINER_NAME
        echo "Contenedor '$CONTAINER_NAME' eliminado."
    else
        echo "El contenedor '$CONTAINER_NAME' no existe."
    fi
}

# Funcion help para dar informacion sobre su uso
help() {
    echo "-create: crea y lanza el contenedor docker con mysql si no existe"
    echo "-start: lanza el contenedor MySql si existe"
    echo "-stop: para el conetendor MySql si existe"
    echo "-delete: borra el contenedor docker si existe"
}

# Verifica el comando pasado al script
case "$1" in
    create)
        create
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    delete)
        delete
        ;;
    help)
        help
        ;;
    *)
        echo "Debe introducir uno de los siguientes parametros para poder hacer alguna accion con el contenedor MySql,"
        echo "Si tiene alguna duda de lo que hacen las acciones use el parametro {help}."
        echo "Uso: $0 {create|start|stop|delete|help}"
        exit 1
        ;;
esac
