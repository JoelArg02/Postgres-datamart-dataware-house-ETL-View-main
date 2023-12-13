import pymysql

# Conexión a la base de datos de origen
source_connection = pymysql.connect(host='source_host', user='user', password='password', db='source_db')

# Conexión a la base de datos de destino (gestion_proyectos)
target_connection = pymysql.connect(host='target_host', user='user', password='password', db='gestion_proyectos')

def extract_data(query, connection):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def transform_data(data):
    # Implementa cualquier lógica de transformación necesaria aquí
    return data

def load_data(query, data, connection):
    with connection.cursor() as cursor:
        cursor.executemany(query, data)
        connection.commit()

# ETL para 'proyectos'
source_data = extract_data("SELECT * FROM external_projects_table", source_connection)
transformed_data = transform_data(source_data)
load_query = "INSERT INTO proyectos (nombre_proyecto, fecha_inicio, fecha_fin, estado) VALUES (%s, %s, %s, %s)"
load_data(load_query, transformed_data, target_connection)

# Repite procesos similares para 'tareas' y 'miembros_equipo'

# Cierra las conexiones
source_connection.close()
target_connection.close()
