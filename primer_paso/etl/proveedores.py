import pymysql

# Conexión a la base de datos de origen
source_connection = pymysql.connect(host='source_host', user='user', password='password', db='source_db')

# Conexión a la base de datos de destino (inventario)
target_connection = pymysql.connect(host='target_host', user='user', password='password', db='inventario')

def extract_data(query, connection):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def transform_proveedores(data):
    # Aquí puedes añadir cualquier lógica de transformación necesaria
    # Por ejemplo, ajustar formatos de datos, limpieza, etc.
    return data

def load_data(query, data, connection):
    with connection.cursor() as cursor:
        cursor.executemany(query, data)
        connection.commit()

# ETL para 'proveedores'
source_data = extract_data("SELECT * FROM external_proveedores_table", source_connection)
transformed_data = transform_proveedores(source_data)
load_query = "INSERT INTO proveedores (nombre_proveedor, direccion, contacto) VALUES (%s, %s, %s)"
load_data(load_query, transformed_data, target_connection)

# Cierra las conexiones
source_connection.close()
target_connection.close()
