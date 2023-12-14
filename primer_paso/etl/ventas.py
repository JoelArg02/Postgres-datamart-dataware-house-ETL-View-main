import pymysql

# Conexión a la base de datos de origen
source_connection = pymysql.connect(host='source_host', user='user', password='password', db='source_db')

# Conexión a la base de datos de destino (ventas)
target_connection = pymysql.connect(host='target_host', user='user', password='password', db='ventas')

def extract_data(query, connection):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def transform_data(data):
    # Aquí puedes añadir cualquier lógica de transformación necesaria
    return data

def load_data(query, data, connection):
    with connection.cursor() as cursor:
        cursor.executemany(query, data)
        connection.commit()

# ETL para la tabla de ventas (ajusta las consultas según tus tablas y datos)
source_data = extract_data("SELECT * FROM external_sales_table", source_connection)
transformed_data = transform_data(source_data)
load_query = "INSERT INTO tu_tabla_ventas (columna1, columna2, ...) VALUES (%s, %s, ...)"
load_data(load_query, transformed_data, target_connection)

# Cierra las conexiones
source_connection.close()
target_connection.close()
