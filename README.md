## API de pedidos
## Descripción

Permite gestionar información relacionada con los técnicos, clientes, y pedidos de la empresa. La aplicación está construida sobre Django y proporciona una serie de endpoints para registrar, actualizar, y consultar técnicos y sus pedidos, así como calcular el monto a cobrar según las horas trabajadas. Además, proporciona informes detallados sobre los pagos y la gestión de los técnicos.
Características principales

    Gestión de Técnicos:
        Permite registrar técnicos con sus datos personales.
        Cálculo del pago de cada técnico según las horas trabajadas y una tabla de tarifas escalonadas.

    Generación de Pedidos:
        Permite la creación masiva de pedidos asignados aleatoriamente a técnicos y clientes, con horas trabajadas definidas.

    Endpoints de Información:
        Listado de Técnicos: Muestra todos los técnicos, con la posibilidad de filtrar por nombre y calcular el total a cobrar.
        Informe de Pagos: Proporciona un informe con el monto promedio cobrado, los técnicos que cobraron por debajo del promedio, y los técnicos con los montos más bajo y más alto.

    Actualización de Pedidos (Opcional):
        Permite modificar detalles de los pedidos ya existentes a través de un servicio web.

    Autenticación:
        Se requiere autenticación para algunos endpoints para asegurar la integridad de los datos.

Requisitos

    Docker: La aplicación utiliza Docker para simplificar la configuración del entorno.
    Django: Framework web utilizado para gestionar la API.
    PostgreSQL (Opcional): Base de datos que se puede configurar dentro de un contenedor Docker.


## Instalar Docker

* Mac, Windows y Ubuntu: [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Docker Desktop Documentation](https://docs.docker.com/desktop/)

### Revisar si el puerto 80 está ocupado. 

Debian:
```bash
netstat -tulpn | grep 80
```
Mac:
```bash
sudo lsof -i :80
```
```bash
docker-compose build
docker-compose up
docker-compose ps

    Name                  Command               State                    Ports                  
------------------------------------------------------------------------------------------------
test-nginx-1  /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp,:::80->80/tcp
app-db            docker-entrypoint.s…"            Up      0.0.0.0:5432->5432/tcp, :::5432->5432/tcp       
test-web-1    python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp

```

```bash
docker exec -it test-web-1 bash
python manage.py  makemigrations
python manage.py  migrate
```
### Cargar datos de pruebas
```bash
docker exec -it test-web-1 bash
python manage.py loaddata app/fixtures/user.json --app app.user
python manage.py loaddata app/fixtures/company.json --app app.company
python manage.py loaddata app/fixtures/scheme.json --app app.scheme
python manage.py loaddata app/fixtures/pedido.json --app app.pedido
python manage.py loaddata app/fixtures/tecnicos.json --app app.tecnicos
```

```bash
docker exec -it test-web-1 bash
python manage.py createsuperuser
```
### Run tests ###
```bash
docker exec -it test-web-1 bash
python manage.py test
```

# Generar pedidos aleatorios #
```bash
docker exec -it test-web-1 bash
python manage.py generate_pedidos <cantidad_de_pedidos>
```

# Endpoints disponibles #

* /api/tecnicos/

Lista de todos los técnicos con los siguientes datos:

    - Nombre completo
    - Horas trabajadas
    - Total a cobrar
    - Cantidad de pedidos en los que trabajó

Opciones de filtrado:

    - Puedes filtrar por first_name y last_name combinados.


* /api/informe-tecnicos/

Devuelve un informe con los siguientes datos:

    - Monto promedio cobrado por los técnicos.
    - Técnicos que cobraron menos que el promedio.
    - Último técnico ingresado que cobró el monto más bajo.
    - Último técnico ingresado que cobró el monto más alto.

* /api/pedidos/

Permite actualizar pedidos mediante el método PUT.
