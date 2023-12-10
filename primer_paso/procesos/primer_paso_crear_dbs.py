import pymongo
import sqlite3
import mysql.connector
import psycopg2

# MongoDB - Redes Sociales
with pymongo.MongoClient("mongodb://localhost:27017/") as mongo_client:
    mongo_db_redes_sociales = mongo_client["redes_sociales"]
    mongo_coleccion_redes_sociales = mongo_db_redes_sociales["usuarios"]

# MongoDB - IoT
with pymongo.MongoClient("mongodb://localhost:27018/") as mongo_client_iot:
    mongo_db_iot = mongo_client_iot["registro_sensores"]
    mongo_coleccion_sensores = mongo_db_iot["lecturas_sensores"]

# MySQL - Recursos Humanos
with mysql.connector.connect(
    host="localhost",
    user="root",
    password="root_password",
    database="recursos_humanos"
) as mysql_conn_recursos_humanos:
    mysql_cursor_recursos_humanos = mysql_conn_recursos_humanos.cursor(dictionary=True)
    mysql_cursor_recursos_humanos.execute("SELECT * FROM empleados")
    mysql_data_empleados = mysql_cursor_recursos_humanos.fetchall()

# MySQL - Ventas
with mysql.connector.connect(
    host="mysql_ventas",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="ventas"
) as mysql_conn_ventas:
    mysql_cursor_ventas = mysql_conn_ventas.cursor(dictionary=True)
    mysql_cursor_ventas.execute("SELECT * FROM clientes")
    mysql_data_clientes_ventas = mysql_cursor_ventas.fetchall()

# MySQL - Inventario
with mysql.connector.connect(
    host="mysql_inventario",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="inventario"
) as mysql_conn_inventario:
    mysql_cursor_inventario = mysql_conn_inventario.cursor(dictionary=True)
    mysql_cursor_inventario.execute("SELECT * FROM productos")
    mysql_data_productos_inventario = mysql_cursor_inventario.fetchall()

# MySQL - Proyectos
with mysql.connector.connect(
    host="mysqli_proyectos",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="gestion_proyectos"
) as mysql_conn_proyectos:
    mysql_cursor_proyectos = mysql_conn_proyectos.cursor(dictionary=True)
    mysql_cursor_proyectos.execute("SELECT * FROM proyectos")
    mysql_data_proyectos = mysql_cursor_proyectos.fetchall()

# MySQL - Facturación
with mysql.connector.connect(
    host="mysqli_facturacion",
    user="tu_usuario_mysql",
    password="tu_contraseña_mysql",
    database="gestion_facturacion"
) as mysql_conn_facturacion:
    mysql_cursor_facturacion = mysql_conn_facturacion.cursor(dictionary=True)
    mysql_cursor_facturacion.execute("SELECT * FROM clientes")
    mysql_data_clientes_facturacion = mysql_cursor_facturacion.fetchall()

# PostgreSQL
with psycopg2.connect(
    host="localhost",
    user="postgres",
    password="password",
    database="ETL-B"
) as postgres_conn:
    postgres_cursor = postgres_conn.cursor()


postgres_conn.commit()
postgres_conn.close()
mongo_client.close()
mongo_client_iot.close()
mysql_conn_recursos_humanos.close()
mysql_conn_ventas.close()
mysql_conn_inventario.close()
mysql_conn_proyectos.close()
mysql_conn_facturacion.close()
