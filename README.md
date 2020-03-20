# CV19_makers_soft_django POC

Fase alpha de aplicación para logística.

Tecnologías utilizadas:

* python 3.7
* Django 2.2.11 (Por ser una LTS)
* Django Rest Framework (Para exponer los datos en una API con JSON)
* PostgreSQL + PostGIS (Para tareas geoespaciales)

# Documentación de la API

* Al arrancar el proyecto cond ocker se puede acceder a `/swagger/` o `/redoc/` que contiene la documentación de los endpoint disponibles


# Arrancar entorno de desarrollo

El sistema propuesto para desarrolo en local es Docker.

* Ejecutar docker-compose up
* Localizar el contenedor de django: `docker ps`

```
CONTAINER ID        IMAGE                                                 COMMAND                   CREATED             STATUS              PORTS                                               NAMES
b1f3325852cf        cv19_makers_soft_django_django_service                "/bin/bash -c '\n    …"   17 hours ago        Up 17 hours         0.0.0.0:8080->80/tcp                                cv19_makers_soft_django_django_service_1
```

* Entrar dentro del contenedor para aplciar las migraciones: `docker exec -it b1f3325852cf bash`
* Una vez dentro, aplicar las migraciones: `python manage migrate`
* Crear un usuario administrador: `python manage createsuperuser`

# Administración de django

La url de acceso para la admin es http://localhost:8080/admin/ y las credenciales son las indicadas con el comando indicado en "Arrancar entorno de desarrollo" (`python manage createsuperuser`)


# Instalación en producción

Los archivos de configuración de ejemplo asumen que la aplicación será instalada en `/var/www/webapp/`. Dentro de `resources/` se encuentran archivos de configuración para nginx y uwsgi.
Los parámetros de configuración de credenciales se encuentran en el archivo .env que deberá ser movido a `src/`. Durante el desarrollo este archivo permanece en un nivel superior del árbol de directorios ya que se comparte con docker.
