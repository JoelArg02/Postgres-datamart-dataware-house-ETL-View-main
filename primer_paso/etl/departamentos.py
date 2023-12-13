import pymysql

# Conexión a la base de datos de origen
source_connection = pymysql.connect(host='source_host', user='user', password='password', db='source_db')

# Conexión a la base de datos de destino (recursos_humanos)
target_connection = pymysql.connect(host='target_host', user='user', password='password', db='recursos_humanos')

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

# ETL para 'departamentos'
source_data = extract_data("SELECT * FROM external_departments_table", source_connection)
transformed_data = transform_data(source_data)
load_query = "INSERT INTO departamentos (nombre_departamento) VALUES (%s)"
load_data(load_query, transformed_data, target_connection)

# Repite procesos similares para 'empleados' y 'historial_salarios'

# Cierra las conexiones
source_connection.close()
target_connection.close()
