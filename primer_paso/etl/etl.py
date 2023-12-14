import pymongo
import psycopg2
from datetime import datetime
import random
import hashlib

def crear_tabla(cursor, consulta, nombre_tabla):
    try:
        cursor.execute(consulta)  # Execute the query passed in 'consulta'
        postgres_conn.commit()    # Commit the transaction
        print(f"Tabla {nombre_tabla} creada con éxito.")
    except psycopg2.Error as e:
        print(f"Error al crear la tabla {nombre_tabla}: {e}")
        postgres_conn.rollback()  # Rollback in case of error


mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["redes"]

mongo_client2 = pymongo.MongoClient("mongodb://localhost:27018")
mongo_db2 = mongo_client2["iot"]

postgres_conn = psycopg2.connect(
    host="localhost",
    database="etlb",
    user="postgres",
    password="password"
)
postgres_cursor = postgres_conn.cursor()

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_iot (
    id_iot INT PRIMARY KEY,
    id_sensor INT,
    fecha TIMESTAMP,
    valor FLOAT
)
""", "dimension_iot")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_usuarios (
    id_usuario INT PRIMARY KEY,
    nombre_usuario VARCHAR(255),
    correo VARCHAR(255)
)
""", "dimension_usuarios")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_publicaciones (
    id_publicacion INT PRIMARY KEY,
    id_usuario INT,
    contenido TEXT,
    fecha_publicacion TIMESTAMP
)
""","dimension_publicaciones")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_facturas (
    id_factura INT PRIMARY KEY,
    nombre_cliente VARCHAR(255),
    fecha_factura TIMESTAMP,
    total_factura FLOAT
)
""", "dimension_facturas")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_categoria (
    id_categoria INT PRIMARY KEY,
    nombre_categoria VARCHAR(255)
)
""","dimension_categoria")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_proovedores (
    id_proovedor INT PRIMARY KEY,
    nombre_proovedor VARCHAR(255)
)
""","dimension_proovedores")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_productos (
    id_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(255),
    id_categoria_producto INT,
    id_proovedor INT,
    precio FLOAT,
    cantidad INT,
    FOREIGN KEY (id_categoria_producto) REFERENCES dimension_categoria(id_categoria),
    FOREIGN KEY (id_proovedor) REFERENCES dimension_proovedores(id_proovedor)
)
""","dimension_productos")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_ventas (
    id_venta INT PRIMARY KEY,
    id_producto INT,
    facurado BOOLEAN,
    FOREIGN KEY (id_producto) REFERENCES dimension_productos(id_producto)
)
""","dimension_ventas")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_proyectos (
    id_proyecto INT PRIMARY KEY,
    nombre_proyecto VARCHAR(255),
    fecha_inicio TIMESTAMP,
    fecha_fin TIMESTAMP,
    completo BOOLEAN
)
""","dimension_proyectos")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_historial_salarios (
    id_historial INT PRIMARY KEY,
    salario_nuevo FLOAT,
    fecha_cambio TIMESTAMP
)
""","dimension_historial_salarios")

crear_tabla(postgres_cursor,"""
CREATE TABLE dimension_empleados (
    id_empleado INT PRIMARY KEY,
    nombre_empleado VARCHAR(255),
    nombre_proyecto VARCHAR(255),
    id_historial INT,
    FOREIGN KEY (id_historial) REFERENCES dimension_historial_salarios(id_historial)
)
""","dimension_empleados")

crear_tabla(postgres_cursor,"""
CREATE TABLE hechos_empresa (
    id_hecho INT PRIMARY KEY,
    id_usuario INT,
    id_producto INT,
    id_tiempo INT,
    id_publicacion INT,
    id_iot INT,
    id_proyecto INT,
    id_factura INT,
    monto_venta FLOAT,
    cantidad_productos INT,
    FOREIGN KEY (id_publicacion) REFERENCES dimension_publicaciones(id_publicacion),
    FOREIGN KEY (id_usuario) REFERENCES dimension_usuarios(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES dimension_productos(id_producto),
    FOREIGN KEY (id_tiempo) REFERENCES dimension_historial_salarios(id_historial),
    FOREIGN KEY (id_iot) REFERENCES dimension_iot(id_iot),
    FOREIGN KEY (id_proyecto) REFERENCES dimension_proyectos(id_proyecto),
    FOREIGN KEY (id_factura) REFERENCES dimension_facturas(id_factura)
)
""","hechos_empresa")

def extraer_datos_sensores_informacion():
    db_iot = mongo_client2["iot"]
    coleccion_sensores_informacion = db_iot["sensores_informacion"]
    datos_sensores_informacion = coleccion_sensores_informacion.find()
    return list(datos_sensores_informacion)

def extraer_datos_lecturas_sensores():
    db_iot = mongo_client2["iot"]
    coleccion_lecturas_sensores = db_iot["lecturas_sensores"]
    datos_lecturas_sensores = coleccion_lecturas_sensores.find()
    return list(datos_lecturas_sensores)

def crear_mapeo_id_sensor(datos_sensores):
    mapeo = {}
    id_sensor = 1  # Comenzar a asignar IDs desde 1
    for sensor in datos_sensores:
        tipo_sensor = sensor['tipo_sensor']
        if tipo_sensor not in mapeo:
            mapeo[tipo_sensor] = id_sensor
            id_sensor += 1
    return mapeo


def transformar_datos_lecturas_sensores(datos_mongo, mapeo_id_sensor):
    datos_transformados = []
    for dato in datos_mongo:
        tipo_sensor = dato['tipo_sensor']
        id_sensor = mapeo_id_sensor.get(tipo_sensor)
        datos_transformados.append({
            'id_sensor': id_sensor,
            'fecha': dato['fecha_lectura'],
            'valor': dato['valor']
        })
    return datos_transformados


def insertar_datos_iot(cursor, datos_iot):
    consulta = "INSERT INTO dimension_iot (id_iot, id_sensor, fecha, valor) VALUES (%s, %s, %s, %s)"
    try:
        for dato in datos_iot:
            cursor.execute(consulta, (dato['id_iot'], dato['id_sensor'], dato['fecha'], dato['valor']))
        postgres_conn.commit()
        print("Datos insertados correctamente en dimension_iot.")
    except psycopg2.Error as e:
        postgres_conn.rollback()
        print(f"Error al insertar datos en dimension_iot: {e}")



datos_sensores = extraer_datos_sensores_informacion()
mapeo_id_sensor = crear_mapeo_id_sensor(datos_sensores)
datos_lecturas_sensores = extraer_datos_lecturas_sensores()
datos_lecturas_sensores_transformados = transformar_datos_lecturas_sensores(datos_lecturas_sensores, mapeo_id_sensor)
insertar_datos_iot(postgres_cursor, datos_lecturas_sensores_transformados)
def extraer_datos_usuarios():
    db_iot = mongo_client2["iot"]
    coleccion_usuarios = db_iot["usuarios"]
    datos_usuarios = coleccion_usuarios.find()
    return list(datos_usuarios)

def transformar_datos_usuarios(datos_mongo):
    datos_transformados = []
    for dato in datos_mongo:
        datos_transformados.append({
            'id_usuario': dato['id_usuario'],
            'nombre_usuario': dato['nombre_usuario'],
            'correo': dato['correo']
        })
    return datos_transformados

def insertar_datos_usuarios(cursor, datos_usuarios):
    consulta = "INSERT INTO dimension_usuarios (id_usuario, nombre_usuario, correo) VALUES (%s, %s, %s)"
    try:
        for dato in datos_usuarios:
            cursor.execute(consulta, (dato['id_usuario'], dato['nombre_usuario'], dato['correo']))
        postgres_conn.commit()
        print("Datos insertados correctamente en dimension_usuarios.")
    except psycopg2.Error as e:
        postgres_conn.rollback()
        print(f"Error al insertar datos en dimension_usuarios: {e}")

# Luego, llamar a estas funciones para realizar el proceso ETL de usuarios
datos_usuarios = extraer_datos_usuarios()
datos_usuarios_transformados = transformar_datos_usuarios(datos_usuarios)
insertar_datos_usuarios(postgres_cursor, datos_usuarios_transformados)

def extraer_datos_facturas():
    coleccion_facturas = mongo_db["facturas"]
    datos_facturas = coleccion_facturas.find()
    return list(datos_facturas)

def transformar_datos_facturas(datos_mongo):
    datos_transformados = []
    for dato in datos_mongo:
        datos_transformados.append({
            'id_factura': dato['id_factura'],
            'nombre_cliente': dato['nombre_cliente'],
            'fecha_factura': dato['fecha_factura'],
            'total_factura': dato['total_factura']
        })
    return datos_transformados

def insertar_datos_facturas(cursor, datos_facturas):
    consulta = "INSERT INTO dimension_facturas (id_factura, nombre_cliente, fecha_factura, total_factura) VALUES (%s, %s, %s, %s)"
    try:
        for dato in datos_facturas:
            cursor.execute(consulta, (dato['id_factura'], dato['nombre_cliente'], dato['fecha_factura'], dato['total_factura']))
        postgres_conn.commit()
        print("Datos insertados correctamente en dimension_facturas.")
    except psycopg2.Error as e:
        postgres_conn.rollback()
        print(f"Error al insertar datos en dimension_facturas: {e}")

# Luego, llamar a estas funciones para realizar el proceso ETL de facturas
datos_facturas = extraer_datos_facturas()
datos_facturas_transformados = transformar_datos_facturas(datos_facturas)
insertar_datos_facturas(postgres_cursor, datos_facturas_transformados)

mongo_client.close()
mongo_client2.close()
postgres_cursor.close()
postgres_conn.close()
